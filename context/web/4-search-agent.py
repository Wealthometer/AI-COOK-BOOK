import json

from openai import OpenAI

from tools import (
    AgentAnswer,
    get_handbook_tool,
    get_web_page,
    get_web_page_tool,
    get_web_search_tool,
    search_handbook,
)

MODEL = "gpt-4.1"
client = OpenAI()

SYSTEM_PROMPT = """You are a research assistant for Dutch government organizations. You can help answer questions by:
1. Searching the AI implementation handbook (for policy questions)
2. Fetching specific web pages (when given a URL)
3. Performing wider web searches (for general information)

Use the most appropriate tool(s) based on the question. Provide clear answers with citations."""

tools = [
    get_handbook_tool(),
    get_web_page_tool(),
    get_web_search_tool(
        allowed_domains=["rijksoverheid.nl", "tweedekamer.nl", "cbs.nl"]
    ),
]


def call_function(name: str, args: dict) -> str:
    """Execute a tool function."""
    if name == "search_handbook":
        return search_handbook(**args)
    elif name == "get_web_page":
        return get_web_page(**args)
    raise ValueError(f"Unknown function: {name}")


def ask_agent(query: str) -> AgentAnswer:
    """Ask the agent a question. It will decide which tools to use."""
    input_messages = [{"role": "user", "content": query}]

    response = client.responses.create(
        model=MODEL,
        input=input_messages,
        tools=tools,
        instructions=SYSTEM_PROMPT,
    )

    tool_calls_made = []
    for output_item in response.output:
        input_messages.append(output_item)

        if output_item.type == "function_call":
            name = output_item.name
            args = json.loads(output_item.arguments)
            print(f"Tool called: {name}")
            if name == "get_web_page":
                print(f"  URL: {args.get('url', 'N/A')}")
            elif name == "search_handbook":
                print(f"  Query: {args.get('query', 'N/A')}")

            result = call_function(name, args)
            tool_calls_made.append(name)

            if name == "get_web_page":
                print(f"  Retrieved {len(result)} characters")
            elif name == "search_handbook":
                print(f"  Handbook retrieved ({len(result)} chars)")

            input_messages.append(
                {
                    "type": "function_call_output",
                    "call_id": output_item.call_id,
                    "output": result,
                }
            )

        # Check for web_search tool usage (built-in tool)
        if output_item.type == "web_search_call":
            print("Tool called: web_search")
            tool_calls_made.append("web_search")

    if not tool_calls_made:
        print("No tool call needed - responding directly")
        final_response = client.responses.parse(
            model=MODEL,
            input=input_messages,
            instructions=SYSTEM_PROMPT,
            text_format=AgentAnswer,
        )
    else:
        print(f"Tools used: {', '.join(tool_calls_made)}")
        while True:
            final_response = client.responses.parse(
                model=MODEL,
                input=input_messages,
                tools=tools,
                instructions=f"{SYSTEM_PROMPT} Use the retrieved information to provide a comprehensive answer. Include 2-4 key citations with text excerpts and sources (URLs or section numbers).",
                text_format=AgentAnswer,
            )

            # Check if there are more tool calls needed
            more_tool_calls = False
            for output_item in final_response.output:
                if output_item.type == "function_call":
                    more_tool_calls = True
                    name = output_item.name
                    args = json.loads(output_item.arguments)
                    print(f"Additional tool called: {name}")

                    result = call_function(name, args)
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
                    return content_item.parsed

    raise ValueError("Could not find parsed response in output")


# Example usage
if __name__ == "__main__":
    examples = [
        {
            "name": "1. No tool call (direct response)",
            "query": "What can you do?",
        },
        {
            "name": "2. Handbook search only",
            "query": "What are the requirements for registering an AI system in the Algorithm Register?",
        },
        {
            "name": "3. Get specific web page",
            "query": "Can you fetch and summarize the content from https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence?",
        },
        {
            "name": "4. Web search only",
            "query": "Use web search to find current policies about AI implementation in Dutch government services on official government websites.",
        },
        {
            "name": "5. Multiple tool calls (handbook + web page)",
            "query": "First, search the handbook for IAMA requirements. Then fetch the EU AI Act page at https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence and compare the requirements.",
        },
    ]

    for example in examples:
        print(f"\n{'=' * 70}")
        print(f"{example['name']}")
        print(f"Query: {example['query']}")
        print(f"{'=' * 70}\n")
        result = ask_agent(example["query"])
        print(f"\nAnswer: {result.answer}\n")
        if result.citations:
            print("Citations:")
            for citation in result.citations:
                source = citation.url or f"Section {citation.section}"
                print(f"  {source}: {citation.text[:100]}...")
        print()
