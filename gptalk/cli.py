"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

from .talk import talk
from .utils import is_url

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
    from .prompt_outline import prompt

    talk(prompt=prompt, data=stdin)

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

    from .prompt_vcard import prompt

    talk(prompt=prompt, data=data)

    sys.exit(0)
