import time
import sys

import openai

from .models import Model


def talk(data: str) -> None:
    """Talk to ChatGPT."""
    with open("vcard_prompt.txt") as f:
        vcard_prompt = "".join(line for line in f).format(userdata=data)

    start_time = time.time()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": vcard_prompt,
            },
            {
                "role": "user",
                "content": str(data),
            },
        ],
        temperature=0,
    )

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
