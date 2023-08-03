"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal

from .talk import talk

deal.activate()


@click.group()
def cli() -> None:
    """Entrypoint for the command-line interface."""


@deal.has("io", "global", "stderr", "stdout")
@click.version_option()
@cli.command()
def vcard() -> NoReturn:
    """Read unstructured data and output a contact card (VCF)."""
    talk(sys.stdin.read())

    sys.exit(0)
