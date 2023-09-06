from time import time
import sys

import openai


def talk(
    prompt_system: str,
    data_user: str,
    model: str = "gpt-3.5-turbo",
) -> None:
    """Talk to ChatGPT."""
    start_time = time()
    request = {
        "temperature": 0,
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": prompt_system,
            },
            {
                "role": "user",
                "content": str(data_user),
            },
        ],
    }

    print(
        f"Sending request:\n{request}",
        file=sys.stderr,
    )
    response = openai.ChatCompletion.create(**request)

    response_time = time() - start_time
    print(
        f"Full response received:\n{response}",
        file=sys.stderr,
    )
    print(
        f"Full response received {response_time:.2f} seconds after request",
        file=sys.stderr,
    )
    print(response.choices[0].message.content.strip())
