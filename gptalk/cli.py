"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

from .talk import talk
from .utils import is_url, fetch_url, summarize
from . import prompts

deal.activate()


@click.group()
@click.version_option()
@deal.has("io")
def cli() -> None:
    """Do some stuff with ChatGPT."""


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def outline() -> NoReturn:
    """Generate MECE outline of an arbitrary topic."""
    stdin = sys.stdin.read().strip()

    talk(prompt_system=prompts.outline, data_user=stdin)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def ticket() -> NoReturn:
    """Create a task ticket using a basic WHAT/WHY/AC format."""
    stdin = sys.stdin.read().strip()

    talk(prompt_system=prompts.ticket, data_user=stdin)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def vcard() -> NoReturn:
    """Read unstructured data and output a contact card (VCF)."""
    stdin = sys.stdin.read().strip()
    if is_url(stdin):
        requests = HTMLSession()

        response = requests.get(url=stdin, timeout=10)
        response.html.render()

        soup = bs(response.content, "lxml")
        data = soup.get_text()
    else:
        data = stdin

    talk(prompt_system=prompts.vcard, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def tldr() -> NoReturn:
    """Provide a tl;dr on a stream."""
    stdin = sys.stdin.read().strip()
    if is_url(stdin):
        if response := fetch_url(stdin):
            data = "\n----\n".join(summarize(response.content.decode()))
    else:
        data = stdin

    talk(prompt_system=prompts.tldr, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def howdoi() -> NoReturn:
    """Like `howdoi` but ChatGPT instead of StackOverflow."""
    data = sys.stdin.read().strip()

    talk(prompt_system=prompts.howdoi, data_user=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def subsfix() -> NoReturn:
    """Fix subtitles generated with speech to text."""
    data = sys.stdin.read().strip()

    talk(prompt_system=prompts.subsfix, data_user=data)

    sys.exit(0)
