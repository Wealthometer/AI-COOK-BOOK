import os

from requests import Session
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import (
    TextFormatter,
)
from youtube_transcript_api.proxies import WebshareProxyConfig

from .utils import extract_video_id


class YouTubeTranscriptService:
    """Service class wrapping youtube-transcript-api with proxy support."""

    def __init__(self, use_proxy: bool = True):
        self.api = self._create_api(use_proxy)

    def _create_api(self, use_proxy: bool) -> YouTubeTranscriptApi:
        """Create API instance with optional proxy support."""
        if not use_proxy:
            return YouTubeTranscriptApi()

        proxy_username = os.getenv("WEBSHARE_USERNAME")
        proxy_password = os.getenv("WEBSHARE_PASSWORD")

        if proxy_username and proxy_password:
            proxy_config = WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_password,
            )
            http_client = Session()
            http_client.proxies = proxy_config.to_requests_dict()
            return YouTubeTranscriptApi(http_client=http_client)

        return YouTubeTranscriptApi()

    def fetch(
        self,
        video_url_or_id: str,
    ):
        """Fetch transcript."""
        video_id = extract_video_id(video_url_or_id)
        return self.api.fetch(video_id)

    def get_transcript_text(
        self,
        video_url_or_id: str,
    ) -> str:
        """Get transcript as plain text."""
        transcript = self.fetch(video_url_or_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
