"""Utility functions and helpers."""
import re
from typing import Tuple

from requests_html import HTMLSession
from requests_html import requests
from readability import Document
from bs4 import BeautifulSoup as bs


def fetch_url(url: str, timeout: int = 10) -> requests.Response:
    """Get the content from a page at URL."""
    requests = HTMLSession()

    response: requests.Response = requests.get(url=url, timeout=10)
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
