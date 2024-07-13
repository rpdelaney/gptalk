"""Utility functions and helpers."""

import re
import sys

from inquirer import Editor, prompt

from .exceptions import GPTNullInputError


def get_input(prompt_message: str = "") -> str:
    """Retrieve some user input."""
    if sys.stdin.isatty():
        questions = [Editor("long_text", message=prompt_message)]
        answers = prompt(questions)
        result = "".join(answers.get("long_text", "")).strip()
    else:
        result = sys.stdin.read().strip()

    if len(result) <= 0:
        msg = "User input was zero-length. Aborting."
        raise GPTNullInputError(msg)

    return result


def is_url(s: str) -> bool:
    """Determine if a given string is a URL.

    Args:
    ----
        s (str): The string to check.

    Returns:
    -------
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
