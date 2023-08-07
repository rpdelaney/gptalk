import time
import sys

import openai

from .utils import strip_html_tags


def talk(
    prompt_filename: str, data: str, model: str = "gpt-3.5-turbo"
) -> None:
    """Talk to ChatGPT."""
    with open(prompt_filename) as f:
        prompt = "".join(line for line in f).format(userdata=data)

    start_time = time.time()
    request = {
        "temperature": 0,
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": strip_html_tags(str(data)),
            },
        ],
    }

    print(
        f"Sending request:\n{request}",
        file=sys.stderr,
    )
    response = openai.ChatCompletion.create(**request)

    response_time = time.time() - start_time
    print(
        f"Full response received:\n{response}",
        file=sys.stderr,
    )
    print(
        f"Full response received {response_time:.2f} seconds after request",
        file=sys.stderr,
    )
    print(response.choices[0].message.content.strip())
