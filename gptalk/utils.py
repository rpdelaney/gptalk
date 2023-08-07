import re

from bs4 import BeautifulSoup, Comment
from typing import Optional


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
