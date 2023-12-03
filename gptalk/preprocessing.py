"""Pre-processors."""
import os
import re
import tempfile
from collections import OrderedDict

import yt_dlp
from bs4 import BeautifulSoup as bs
from readability import Document
from requests import Response
from requests_html import HTMLSession

from .exceptions import GPTSubsNotFoundError


def fetch_url(url: str, timeout: int = 10) -> str:
    """Get the content from a page at URL."""
    requests = HTMLSession()

    response: Response = requests.get(url=url, timeout=10)
    response.html.render()
    response.raise_for_status()

    return response.content.decode()


def summarize(content: str) -> tuple[str, str]:
    """Take content and use readability to return a document summary."""
    doc = Document(content)

    title: str = doc.short_title()
    summary: str = bs(doc.summary(), "lxml").text

    return (title, summary)


def extract_subtitles(url: str) -> str:
    """Extract subtitles from a URL, if supported.

    Extract automatic subtitles from a string that could be a video URL
    using yt_dlp.

    This function first checks if the provided string is a URL supported by
    a yt_dlp extractor. If it is, it attempts to extract and process
    subtitles from the video at that URL. If not, it simply returns the
    original string.

    Args:
        url (str): The string to check and process if it's a supported
        URL.

    Returns:
        str: The extracted and processed subtitles as a string, or the
        original string if it's not a supported URL.
    """
    for extractor in yt_dlp.extractor.gen_extractors():
        if extractor.suitable(url):
            break
    else:
        return url

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

    try:
        with open(subs_filename, "r", encoding="utf-8") as file:
            subtitles = file.read()
    except FileNotFoundError as fnfe:
        raise GPTSubsNotFoundError("No subtitles found.") from fnfe

    return vtt2prose(subtitles)
