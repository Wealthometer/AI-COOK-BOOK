# --------------------------------------------------------------
# Search Handbook with Dynamic Tool Calls
# --------------------------------------------------------------

import json
from pathlib import Path
from typing import List

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

MODEL = "gpt-4.1-nano"
HANDBOOK_PATH = Path(__file__).parent / "data" / "handbook.md"


# --------------------------------------------------------------
# Define the output models
# --------------------------------------------------------------


class Citation(BaseModel):
    text: str
    section: str


class HandbookAnswer(BaseModel):
    answer: str
    citations: List[Citation]


# --------------------------------------------------------------
# Handbook search function (called as a tool)
# --------------------------------------------------------------


def search_handbook(query: str) -> str:
    """Retrieve the handbook content for the agent to interpret.

    Note: The query parameter is accepted but not used - we return the full handbook.
    This simulates Retrieval Augmented Generation (RAG). In a real application with
    large handbooks or contexts, you would implement semantic search, filtering, or
    chunking to retrieve only relevant sections based on the query.

    Returns: The full handbook content as a string
    """
    if not HANDBOOK_PATH.exists():
        return "Handbook not found."

    handbook_content = HANDBOOK_PATH.read_text(encoding="utf-8")
    return handbook_content


# --------------------------------------------------------------
# Define the tool
# --------------------------------------------------------------

tools = [
    {
        "type": "function",
        "name": "search_handbook",
        "description": "Retrieve the AI implementation handbook content. Use this when the user asks questions about AI implementation requirements, regulations, or procedures. The handbook contains policies, regulations, and guidelines for Dutch government organizations.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question or query - used for context, but the full handbook will be returned",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


# --------------------------------------------------------------
# Agent function that uses tools dynamically
# --------------------------------------------------------------


def call_function(name: str, args: dict) -> str:
    if name == "search_handbook":
        return search_handbook(**args)
    raise ValueError(f"Unknown function: {name}")


def ask_agent(query: str) -> HandbookAnswer:
    """Ask the agent a question. It will decide whether to search the handbook."""
    input_messages = [{"role": "user", "content": query}]

    response = client.responses.create(
        model=MODEL,
        input=input_messages,
        tools=tools,
        instructions="You are a helpful assistant for Dutch government organizations. You can help answer questions about AI implementation policies and regulations by searching the handbook. If asked what you can do, simply explain your capabilities without searching the handbook.",
    )

    tool_calls_made = False
    # Append all output items in order to preserve reasoning relationships
    for output_item in response.output:
        # Append the output item first (includes reasoning if present)
        input_messages.append(output_item)

        if output_item.type == "function_call":
            tool_calls_made = True
            name = output_item.name
            args = json.loads(output_item.arguments)
            print(f"Tool called: {name}")
            result = call_function(name, args)
            print(f"Handbook retrieved ({len(result)} chars)")

            # Append function call output after the function call
            input_messages.append(
                {
                    "type": "function_call_output",
                    "call_id": output_item.call_id,
                    "output": result,
                }
            )

    if not tool_calls_made:
        print("No tool call needed, responding directly\n")
        # For direct responses, return structured output without citations
        direct_response = client.responses.parse(
            model=MODEL,
            input=input_messages,
            instructions="You are a helpful assistant for Dutch government organizations.",
            text_format=HandbookAnswer,
        )
        return direct_response.output[-1].content[-1].parsed

    final_response = client.responses.parse(
        model=MODEL,
        input=input_messages,
        tools=tools,
        instructions="You are a helpful assistant for Dutch government organizations. Use the handbook content that was retrieved to answer the user's question. Provide a clear, comprehensive answer. Include only the most important citations (2-4 maximum) that reference the primary sections where the key information comes from. Each citation should include a brief text excerpt and the section number (e.g., '2.1', '3.2'). Do not cite every detail - only cite the main sources.",
        text_format=HandbookAnswer,
    )

    return final_response.output[-1].content[-1].parsed


# --------------------------------------------------------------
# Example queries
# --------------------------------------------------------------

example_queries = [
    "What can you do?",
    "What are the requirements for registering an AI system in the Algorithm Register?",
    "Do I need to perform an IAMA for a chatbot that answers citizen questions?",
]

# Test with example queries
if __name__ == "__main__":
    for query in example_queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"{'=' * 60}\n")
        result = ask_agent(query)
        print(f"Answer: {result.answer}\n")
        if result.citations:
            print("Citations:")
            for citation in result.citations:
                print(f"  Section {citation.section}: {citation.text[:100]}...")
        print()
