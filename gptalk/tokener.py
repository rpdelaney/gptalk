"""Helpers for meeting the token limits."""

import sys

import deal
import tiktoken
from tiktoken.core import Encoding


_DEFAULT_ENCODING: Encoding = tiktoken.get_encoding("cl100k_base")


@deal.pure
def token_split(
    text: str,
    limit: int,
    encoding: Encoding = _DEFAULT_ENCODING,
) -> list[str]:
    """Split a string into parts of given size without breaking words.

    Args:
    ----
        text (str): Text to split.
        limit (int): Maximum number of tokens per part.
        encoding (tiktoken.Encoding): Encoding to use for tokenization.

    Returns:
    -------
        list[str]: List of text parts.

    """
    tokens = encoding.encode(text)
    parts = []
    text_parts = []
    current_part = []
    current_count = 0

    for token in tokens:
        current_part.append(token)
        current_count += 1

        if current_count >= limit:
            parts.append(current_part)
            current_part = []
            current_count = 0

    if current_part:
        parts.append(current_part)

    # Convert the tokenized parts back to text
    for part in parts:
        text = [
            encoding.decode_single_token_bytes(token).decode(
                "utf-8", errors="replace"
            )
            for token in part
        ]
        text_parts.append("".join(text))

    return text_parts


@deal.pure
def get_token_count(text: str, encoding: Encoding = _DEFAULT_ENCODING) -> int:
    """Get the number of tokens in the input string using tiktoken library.

    Args:
    ----
        s (str): The input string.

    Returns:
    -------
        int: The number of tokens in the string.

    >>> get_token_count("Hello, World!")
    3

    """
    tokens = encoding.encode(text)
    return len(tokens)


@deal.has("io", "read", "stdout")
@deal.safe
def main() -> None:
    """Give example usage."""
    limit = int(sys.argv[1])

    with open(sys.argv[2]) as f:
        text = "\n".join(line for line in f)

    split_content = token_split(text, limit, _DEFAULT_ENCODING)
    for line in split_content:
        print(line)
        print("-" * 79)
    print(f"Number of splits: {len(split_content)}")


if __name__ == "__main__":
    main()
