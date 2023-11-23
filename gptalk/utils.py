"""Utility functions and helpers."""
import os
import re
from typing import Tuple
import tempfile
from collections import OrderedDict

from requests_html import HTMLSession
from requests import Response
from readability import Document
from bs4 import BeautifulSoup as bs
import yt_dlp


def fetch_url(url: str, timeout: int = 10) -> Response:
    """Get the content from a page at URL."""
    requests = HTMLSession()

    response: Response = requests.get(url=url, timeout=10)
    response.html.render()
    response.raise_for_status()

    return response


def summarize(content: str) -> Tuple[str, str]:
    """Take content and use readability to return a document summary."""
    doc = Document(content)

    title: str = doc.short_title()
    summary: str = bs(doc.summary(), "lxml").text

    return (title, summary)


def is_url(s: str) -> bool:
    """Determine if a given string is a URL.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a URL, False otherwise.

    >>> is_url("https://www.openai.com")
    True
    >>> is_url("ftp://files.example.com")
    True
    >>> is_url("Not a URL")
    False
    """
    pattern = (
        r"http[s]?://"
        r"(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|"
        r"(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return bool(re.match(pattern, s))


def extract_subtitles(url: str) -> str:
    """
    Extract automatic subtitles from a video URL using yt_dlp, save to a
    temporary file, and return as a string.

    Args:
        url (str): The URL of the video.

    Returns:
        str: The extracted subtitles as a string.
    """

    def vtt2prose(vtt: str) -> str:
        """
        Process VTT subtitles into prose.

        Returns:
            str: The processed prose from the VTT subtitles.
        """
        lines_seen: OrderedDict[str, None] = OrderedDict()
        for line in vtt.splitlines():
            processed_line = re.sub(r"<[^>]+>", "", line)
            if (
                processed_line
                and not processed_line.startswith("WEBVTT")
                and "-->" not in processed_line
            ):
                lines_seen[processed_line] = None
        return " ".join(lines_seen.keys()).strip()

    class YtLogger:
        def debug(self, msg: str) -> None:
            pass

        def warning(self, msg: str) -> None:
            pass

        def error(self, msg: str) -> None:
            print(msg)

    temp_dir = tempfile.TemporaryDirectory()
    ydl_opts = {
        "format": "best",
        "skip_download": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "logger": YtLogger(),
        "outtmpl": os.path.join(temp_dir.name, "%(id)s.%(ext)s"),
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get("id")
        subs_filename = os.path.join(temp_dir.name, f"{video_id}.en.vtt")

    with open(subs_filename, "r", encoding="utf-8") as file:
        subtitles = file.read()

    return vtt2prose(subtitles)
