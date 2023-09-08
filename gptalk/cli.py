"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from inquirer import prompt, Text

from .talk import talk
from .utils import is_url, fetch_url, summarize
from . import prompts

deal.activate()


def _get_input(prompt_message: str) -> str:
    if sys.stdin.isatty():
        questions = [Text("input", message=prompt_message)]
        answers = prompt(questions)
        return "".join(answers["input"])
    else:
        return sys.stdin.read().strip()


@click.group()
@click.version_option()
@deal.has("io")
def cli() -> None:
    """Do some stuff with ChatGPT."""


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def outline() -> NoReturn:
    """Generate MECE outline of an arbitrary topic."""
    input_user = _get_input("Please provide input:")
    talk(prompt_system=prompts.outline, data_user=input_user)
    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def ticket() -> NoReturn:
    """Create a task ticket using a basic WHAT/WHY/AC format."""
    input_user = _get_input("Please provide input:")

    talk(prompt_system=prompts.ticket, data_user=input_user)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def vcard() -> NoReturn:
    """Read unstructured data and output a contact card (VCF)."""
    input_user = _get_input("Please provide input:")
    if is_url(input_user):
        data = summarize(fetch_url(input_user))
    else:
        data = input_user

    talk(prompt_system=prompts.vcard, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def tldr() -> NoReturn:
    """Provide a tl;dr on a stream."""
    input_user = _get_input("Please provide input:")
    if is_url(input_user):
        if response := fetch_url(input_user):
            data = "\n----\n".join(summarize(response.content.decode()))
    else:
        data = input_user

    talk(prompt_system=prompts.tldr, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def howdoi() -> NoReturn:
    """Like `howdoi` but ChatGPT instead of StackOverflow."""
    data = _get_input("Please provide input:")

    talk(prompt_system=prompts.howdoi, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def subsfix() -> NoReturn:
    """Fix subtitles generated with speech to text."""
    data = _get_input("Please provide input:")

    talk(prompt_system=prompts.subsfix, data_user=data)

    sys.exit(0)
