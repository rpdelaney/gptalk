"""Entrypoint for the command-line interface."""
import sys
from typing import NoReturn

import click
import deal

from .talk import talk

deal.activate()


@deal.has("io", "global", "stderr", "stdout")
@click.version_option()
def cli() -> NoReturn:
    """Entrypoint for the command-line interface."""
    talk(sys.stdin.read())

    sys.exit(0)
