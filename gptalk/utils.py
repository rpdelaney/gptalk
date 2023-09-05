"""Utility functions and helpers."""
import re
from typing import Tuple

from readability import Document
from bs4 import BeautifulSoup as bs


def summarize(content: str) -> Tuple[str, str]:
    """Take content and use readability to return a document summary."""
    doc = Document(content)

    title = doc.title()
    summary = bs(doc.summary(), "lxml")

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
