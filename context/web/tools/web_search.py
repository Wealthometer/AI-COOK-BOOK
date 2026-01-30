def get_tool_definition(allowed_domains: list = None):
    """Get web search tool definition for responses API."""
    tool = {
        "type": "web_search",
    }
    if allowed_domains:
        tool["filters"] = {"allowed_domains": allowed_domains}
    return tool

