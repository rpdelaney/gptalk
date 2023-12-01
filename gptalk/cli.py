"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal
from requests_html import HTMLSession

from . import prompts
from .constants import GPT_MODEL_DEFAULT
from .postprocessing import tldr_to_markdown, unfence
from .preprocessing import extract_subtitles, fetch_url, summarize
from .talk import talk
from .utils import is_url, get_input

deal.activate()


@click.group()
@click.version_option()
def cli() -> None:
    """Do some stuff with ChatGPT."""


@cli.command()
def outline() -> NoReturn:
    """Generate MECE outline of an arbitrary topic."""
    input_user = get_input()
    print(
        talk(
            prompt_system=prompts.outline,
            data_user=input_user,
            model=GPT_MODEL_DEFAULT,
        )
    )
    sys.exit(0)


@cli.command()
def ticket() -> NoReturn:
    """Create a task ticket using a basic WHAT/WHY/AC format."""
    input_user = get_input()

    print(
        talk(
            prompt_system=prompts.ticket,
            data_user=input_user,
            model=GPT_MODEL_DEFAULT,
        )
    )

    sys.exit(0)


@cli.command()
def vcard() -> NoReturn:
    """Read unstructured data and output a contact card (VCF)."""
    input_user = get_input()
    if is_url(input_user):
        if response := fetch_url(input_user):
            data = "\n----\n".join(summarize(response.content.decode()))
    else:
        data = input_user

    print(
        talk(
            prompt_system=prompts.vcard,
            data_user=data,
            model="gpt-3.5-turbo-16k",
        )
    )

    sys.exit(0)


@cli.command()
def tldr() -> NoReturn:
    """Provide a tl;dr on a stream."""
    input_user = get_input()
    if is_url(input_user):
        if "youtu" in input_user:
            data = extract_subtitles(input_user)
        elif response := fetch_url(input_user):
            data = "\n----\n".join(summarize(response.content.decode()))
    else:
        data = input_user

    result = talk(
        prompt_system=prompts.tldr,
        data_user=data,
        model=GPT_MODEL_DEFAULT,
        postprocessors=[unfence, tldr_to_markdown],
    )
    print(result)

    sys.exit(0)


@cli.command()
def howdoi() -> NoReturn:
    """Like `howdoi` but ChatGPT instead of StackOverflow."""
    data = get_input()

    print(
        talk(
            prompt_system=prompts.howdoi,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
        )
    )

    sys.exit(0)


@cli.command()
def subsfix() -> NoReturn:
    """Fix subtitles generated with speech to text."""
    data = get_input()

    print(talk(prompt_system=prompts.subsfix, data_user=data))

    sys.exit(0)
