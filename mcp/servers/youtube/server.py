# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp[cli]>=1.12.3",
#     "pydantic>=2.11.7",
#     "python-dotenv>=1.1.1",
#     "requests>=2.32.4",
#     "youtube-transcript-api>=1.2.2",
# ]
# ///


from mcp.server.fastmcp import FastMCP
from src.service import YouTubeTranscriptService

mcp = FastMCP(
    name="YouTube",
    stateless_http=True,
)

_service = YouTubeTranscriptService(use_proxy=True)


@mcp.tool()
def get_transcript(
    video_url_or_id: str,
) -> str:
    """Get transcript as plain text."""
    try:
        return _service.get_transcript_text(video_url_or_id)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
