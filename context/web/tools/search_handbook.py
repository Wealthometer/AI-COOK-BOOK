from pathlib import Path

HANDBOOK_PATH = Path(__file__).parent.parent / "data" / "handbook.md"


def search_handbook(query: str) -> str:
    """Retrieve the handbook content for the agent to interpret.

    Note: The query parameter is accepted but not used - we return the full handbook.
    This simulates Retrieval Augmented Generation (RAG). In a real application with
    large handbooks or contexts, you would implement semantic search, filtering, or
    chunking to retrieve only relevant sections based on the query.
    """
    if not HANDBOOK_PATH.exists():
        return "Handbook not found."
    return HANDBOOK_PATH.read_text(encoding="utf-8")


def get_tool_definition():
    return {
        "type": "function",
        "name": "search_handbook",
        "description": "Retrieve the AI implementation handbook content. Use this when the user asks questions about AI implementation requirements, regulations, or procedures.",
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
