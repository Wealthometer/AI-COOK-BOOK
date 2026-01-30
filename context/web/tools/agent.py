import json
import os
from typing import List

from openai import OpenAI

from dotenv import load_dotenv

from .get_web_page import get_web_page, get_tool_definition as get_web_page_tool
from .models import AgentAnswer
from .search_handbook import search_handbook, get_tool_definition as get_handbook_tool
from .web_search import get_tool_definition as get_web_search_tool


DEFAULT_SYSTEM_PROMPT = """You are a research assistant for Dutch government organizations. You can help answer questions by:
1. Searching the AI implementation handbook (for policy questions)
2. Fetching specific web pages (when given a URL)
3. Performing wider web searches (for general information)

Use the most appropriate tool(s) based on the question. Provide clear answers with citations."""


class SearchAgent:
    """Multi-source search agent with conversation history."""

    def __init__(
        self,
        model: str = "gpt-4.1",
        system_prompt: str = None,
        verbose: bool = True,
    ):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.verbose = verbose
        self.conversation_history: List[dict] = []
        self._last_tool_calls: List[dict] = []

        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

        self.tools = [
            get_handbook_tool(),
            get_web_page_tool(),
            get_web_search_tool(
                allowed_domains=["rijksoverheid.nl", "tweedekamer.nl", "cbs.nl"]
            ),
        ]

    def _call_function(self, name: str, args: dict) -> str:
        """Execute a tool function."""
        if name == "search_handbook":
            return search_handbook(**args)
        elif name == "get_web_page":
            return get_web_page(**args)
        raise ValueError(f"Unknown function: {name}")

    def _log(self, message: str):
        """Print log message if verbose."""
        if self.verbose:
            print(message)

    def ask(self, query: str) -> AgentAnswer:
        """Ask the agent a question. Maintains conversation history."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": query})

        # Start with conversation history
        input_messages = self.conversation_history.copy()

        # Initial response with tools
        response = self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=self.tools,
            instructions=self.system_prompt,
        )

        tool_calls_made = []
        for output_item in response.output:
            input_messages.append(output_item)

            if output_item.type == "function_call":
                name = output_item.name
                args = json.loads(output_item.arguments)
                self._log(f"Tool called: {name}")
                if name == "get_web_page":
                    self._log(f"  URL: {args.get('url', 'N/A')}")
                elif name == "search_handbook":
                    self._log(f"  Query: {args.get('query', 'N/A')}")

                result = self._call_function(name, args)
                tool_calls_made.append(name)

                if name == "get_web_page":
                    self._log(f"  Retrieved {len(result)} characters")
                elif name == "search_handbook":
                    self._log(f"  Handbook retrieved ({len(result)} chars)")

                input_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": output_item.call_id,
                        "output": result,
                    }
                )

            if output_item.type == "web_search_call":
                self._log("Tool called: web_search")
                tool_calls_made.append("web_search")

        # Get final answer
        if not tool_calls_made:
            self._log("No tool call needed - responding directly")
            final_response = self.client.responses.parse(
                model=self.model,
                input=input_messages,
                instructions=self.system_prompt,
                text_format=AgentAnswer,
            )
        else:
            self._log(f"Tools used: {', '.join(tool_calls_made)}")
            while True:
                final_response = self.client.responses.parse(
                    model=self.model,
                    input=input_messages,
                    tools=self.tools,
                    instructions=f"{self.system_prompt} Use the retrieved information to provide a comprehensive answer. Include 2-4 key citations with text excerpts and sources (URLs or section numbers).",
                    text_format=AgentAnswer,
                )

                more_tool_calls = False
                for output_item in final_response.output:
                    if output_item.type == "function_call":
                        more_tool_calls = True
                        name = output_item.name
                        args = json.loads(output_item.arguments)
                        self._log(f"Additional tool called: {name}")

                        result = self._call_function(name, args)
                        input_messages.append(output_item)
                        input_messages.append(
                            {
                                "type": "function_call_output",
                                "call_id": output_item.call_id,
                                "output": result,
                            }
                        )

                if not more_tool_calls:
                    break

        # Extract parsed content
        for output_item in reversed(final_response.output):
            if hasattr(output_item, "content") and output_item.content:
                for content_item in reversed(output_item.content):
                    if hasattr(content_item, "parsed") and content_item.parsed:
                        answer = content_item.parsed
                        # Add assistant response to history
                        self.conversation_history.append(
                            {"role": "assistant", "content": answer.answer}
                        )
                        return answer

        raise ValueError("Could not find parsed response in output")
