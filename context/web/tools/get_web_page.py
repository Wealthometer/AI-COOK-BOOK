from docling.document_converter import DocumentConverter

converter = DocumentConverter()


def get_web_page(url: str) -> str:
    """Fetch and convert a web page to markdown."""
    page_content = converter.convert(url)
    return page_content.document.export_to_markdown()


def get_tool_definition():
    return {
        "type": "function",
        "name": "get_web_page",
        "description": "Fetch and retrieve the content of a specific web page given its URL. Use this when you need to read a particular webpage.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to fetch",
                },
            },
            "required": ["url"],
            "additionalProperties": False,
        },
        "strict": True,
    }
