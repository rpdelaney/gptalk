"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

from .talk import talk
from .utils import is_url
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

    talk(prompt=prompts.outline, data=stdin)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def ticket() -> NoReturn:
    """Create a task ticket using a basic WHAT/WHY/AC format."""
    stdin = sys.stdin.read().strip()

    talk(prompt=prompts.ticket, data=stdin)

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

    talk(prompt=prompts.vcard, data=data)

    sys.exit(0)


@deal.has("io", "global", "stderr", "stdout")
@cli.command()
def tldr() -> NoReturn:
    """Provide a tl;dr on a stream."""
    stdin = sys.stdin.read().strip()
    if is_url(stdin):
        requests = HTMLSession()

        response = requests.get(url=stdin, timeout=10)
        response.html.render()

        soup = bs(response.content, "lxml")
        data = soup.get_text()
    else:
        data = stdin

    talk(prompt=prompts.tldr, data=data)

    sys.exit(0)
