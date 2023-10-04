from time import time
import os
import sys

import openai
import deal
from openai.openai_object import OpenAIObject


@deal.has('io', 'stdout')
@deal.safe
def debug(msg: str, file=sys.stderr) -> None:
    """Print a debug message if $DEBUG is set."""
    if os.getenv("DEBUG"):
        print(msg)


@deal.has('io', 'stderr', 'stdout', 'time')
@deal.safe
def talk(
    prompt_system: str,
    data_user: str,
    model: str = "gpt-3.5-turbo-16k",
) -> None:
    """Initiate a conversation with the specified model.

    :param prompt_system: The system prompt to initiate the conversation.
    :param data_user: The input data from the user for the system prompt
    to act on.
    :param model: The model to be used for the conversation, default is
    "gpt-3.5-turbo".

    :return: None
    """
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

    print("Sending request...", file=sys.stderr)
    debug(f"{request}")

    response: OpenAIObject = openai.ChatCompletion.create(**request)

    response_time = time() - start_time
    debug(
        f"Full response received:\n{response}",
        file=sys.stderr,
    )
    debug(
        f"Full response received {response_time:.2f} seconds after request",
        file=sys.stderr,
    )
    print(response.choices[0].message.content.strip())
