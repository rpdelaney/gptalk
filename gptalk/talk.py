import time
import sys

import openai


def talk(
    prompt_filename: str, data: str, model: str = "gpt-3.5-turbo"
) -> None:
    """Talk to ChatGPT."""
    with open(prompt_filename) as f:
        vcard_prompt = "".join(line for line in f).format(userdata=data)

    start_time = time.time()

    response = openai.ChatCompletion.create(
        model=model,
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
