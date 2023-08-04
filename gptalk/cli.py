"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal

from .talk import talk

deal.activate()


@click.group()
def cli() -> None:
    """Do some stuff with ChatGPT."""


@deal.has("io", "global", "stderr", "stdout")
@click.version_option()
@cli.command()
def vcard() -> NoReturn:
    """Read unstructured data and output a contact card (VCF)."""
    talk(prompt_filename="vcard_prompt.txt", data=sys.stdin.read())

    sys.exit(0)
