"""Pre-processors."""

import contextlib
import io
import re
import tempfile
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urlparse

import requests
import yt_dlp
from bs4 import BeautifulSoup as Bs
from pdftotext import PDF
from readability import Document
from yt_dlp.utils import DownloadError

from .utils import is_url


def fetch_url(url: str, timeout: int = 10) -> str:
    """Get the content from a page at URL, if it is a URL."""
    if not is_url(url):
        return url

    response = requests.get(
        url,
        timeout=timeout,
        headers={
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Host": urlparse(url).netloc,
            "TE": "trailers",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; rv:109.0) "
                "Gecko/20100101 Firefox/115.0"
            ),
            "COOKIE": "p=-2",
            "SEC-FETCH-DEST": "document",
            "SEC-FETCH-MODE": "navigate",
            "SEC-FETCH-SITE": "none",
            "SEC-FETCH-USER": "?1",
            "UPGRADE-INSECURE-REQUESTS": "1",
        },
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type")

    if content_type == "application/pdf":
        text = "\n\n".join(PDF(io.BytesIO(response.content)))
        return str(text)

    soup = Bs(response.content, "html.parser")

    return soup.get_text()


def summarize(content: str) -> str:
    """Take content and use readability to return a document summary."""
    doc = Document(content)

    title: str = doc.short_title()
    summary: str = Bs(doc.summary(), "lxml").text

    return f"{title}\n{summary}"


def extract_subtitles(url: str) -> str:
    """Extract subtitles from a URL, if supported.

    Extract automatic subtitles from a string that could be a video URL
    using yt_dlp.

    This function first checks if the provided string is a URL supported by
    a yt_dlp extractor. If it is, it attempts to extract and process
    subtitles from the video at that URL. If not, it simply returns the
    original string.

    Args:
    ----
        url (str): The string to check and process if it's a supported
        URL.

    Returns:
    -------
        str: The extracted and processed subtitles as a string, or the
        original string if it's not a supported URL.

    """
    for extractor in yt_dlp.extractor.gen_extractors():
        # The generic extractor always returns suitable, even
        # when it won't run on the URL
        if extractor.suitable(url) and extractor.IE_NAME != "generic":
            break
    else:
        return url

    def vtt2prose(vtt: str) -> str:
        """Process VTT subtitles into prose.

        Returns
        -------
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
        "skip_download": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "logger": YtLogger(),
        "outtmpl": str(Path(temp_dir.name) / Path("%(id)s.%(ext)s")),
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get("id")
            subs_filename = Path(temp_dir.name) / Path(f"{video_id}.en.vtt")
    except DownloadError:
        return url

    subtitles = ""
    with (
        contextlib.suppress(FileNotFoundError),
        Path.open(subs_filename, encoding="utf-8") as file,
    ):
        subtitles = file.read()

    return vtt2prose(subtitles) if subtitles else url
