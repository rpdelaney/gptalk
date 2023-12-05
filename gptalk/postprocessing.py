"""Post-processors."""
import json
import re
from json.decoder import JSONDecodeError
from typing import Callable

from .exceptions import GPTJSONDecodeError

T_Postprocessor = Callable[[str], str]


def unfence(text: str) -> str:
    """
    Remove triple backticks from a multi-line string.

    :param text: A string that may have fenced code blocks.
    :return: A string without fenced code blocks.
    """
    return re.sub(
        r"^```(\s*\w+)?$",
        "",
        text.strip(),
        flags=re.MULTILINE,
    )


def tldr_to_markdown(json_data: str) -> str:
    """
    Convert a JSON string with a tldr response to Markdown format.

    :param json_data: A JSON string with a tldr.
    :return: A string in Markdown format.

    >>> data = '{"title": "Example Title", "description": "Example Description", "key_points": ["Point 1", "Point 2"]}'
    >>> print(json_to_markdown(data))
    # Example Title

    Example Description

    ## Key points

    - Point 1
    - Point 2
    """
    try:
        data = json.loads(json_data)
    except JSONDecodeError as jde:
        raise GPTJSONDecodeError(
            f"Data was: {json_data}",
            doc=jde.doc,
            pos=jde.pos,
        ) from jde

    markdown_text = f"# {data['title']}\n\n"
    markdown_text += f"{data['description']}\n\n"
    markdown_text += "## Key points\n\n"
    markdown_text += "\n".join(f"- {point}" for point in data["key_points"])

    return markdown_text
