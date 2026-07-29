#!/usr/bin/env python3
"""Extract transcript content using interchangeable source strategies."""
# pylint: disable=too-few-public-methods
import argparse
import json
import os
import sys
from abc import ABC, abstractmethod
from xml.etree import ElementTree

import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig


class TranscriptExtractor(ABC):
    """Define the contract for transcript extraction strategies."""

    @abstractmethod
    def fetch_raw_string(self, source_id: str) -> str:
        """Return raw transcript text for a source identifier."""


class YouTubeExtractor(TranscriptExtractor):
    """Extract transcript text from YouTube videos."""

    def __init__(
        self,
        proxy_username: str | None = None,
        proxy_password: str | None = None,
    ):
        """Create a YouTube API client with optional Webshare routing."""
        if proxy_username and proxy_password:
            self.ytt_api = YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    proxy_username=proxy_username,
                    proxy_password=proxy_password,
                )
            )
        else:
            self.ytt_api = YouTubeTranscriptApi()

    def fetch_raw_string(self, source_id: str) -> str:
        """Fetch and combine transcript segments for a YouTube video."""
        fetched_transcript = self.ytt_api.fetch(source_id)
        transcript_list = fetched_transcript.to_raw_data()

        return " ".join(
            f"[{item['start']}] {item['text']}"
            for item in transcript_list
        )


class PodcastRssExtractor(TranscriptExtractor):
    """Extract podcast show notes from an RSS feed."""

    def __init__(self, feed_url: str):
        """Store the RSS feed URL used for podcast extraction."""
        self.feed_url = feed_url

    def fetch_raw_string(self, source_id: str) -> str:
        """Find podcast show notes matching a supplied identifier."""
        response = requests.get(self.feed_url, timeout=10)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)

        for item in root.findall(".//item"):
            title_element = item.find("title")
            description_element = item.find("description")

            if title_element is None or description_element is None:
                continue

            title_text = title_element.text or ""
            description_text = description_element.text or ""

            if source_id.lower() in title_text.lower():
                return (
                    f"[LIVE PODCAST SHOW NOTES - {title_text}]: "
                    f"{description_text}"
                )

        raise ValueError(
            f"No podcast episode matching '{source_id}' was found."
        )


class ExtractionEngine:
    """Process standard-input identifiers with an extraction strategy."""

    def __init__(self, strategy: TranscriptExtractor):
        """Store the extraction strategy used by the engine."""
        self.strategy = strategy

    def run_stream(self) -> None:
        """Read identifiers from stdin and emit transcript JSONL records."""
        for line in sys.stdin:
            source_id = line.strip()

            if not source_id:
                continue

            try:
                raw_text = self.strategy.fetch_raw_string(source_id)

                payload = {
                    "video_id": source_id,
                    "raw_text": raw_text,
                }

                sys.stdout.write(json.dumps(payload) + "\n")
                sys.stdout.flush()

            except Exception as error:  # pylint: disable=broad-exception-caught
                sys.stderr.write(
                    f"ERROR processing token [{source_id}]: {error}\n"
                )
                sys.stderr.flush()


def main(argv=None) -> None:
    """Select an extraction strategy and process standard input."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Multi-source transcript ingestion node."
    )

    parser.add_argument(
        "--source",
        choices=["youtube", "podcast"],
        default="youtube",
        help="Select the transcript source strategy.",
    )

    parser.add_argument(
        "--feed-url",
        default="https://talkpython.fm/episodes/rss",
        help="RSS feed used by the podcast strategy.",
    )

    args = parser.parse_args(argv)

    if args.source == "youtube":
        selected_strategy = YouTubeExtractor(
            proxy_username=os.getenv("WEBSHARE_USER"),
            proxy_password=os.getenv("WEBSHARE_PASSWORD"),
        )
    else:
        selected_strategy = PodcastRssExtractor(
            feed_url=args.feed_url
        )

    engine = ExtractionEngine(selected_strategy)
    engine.run_stream()


if __name__ == "__main__":
    main()
