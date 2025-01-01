"""Entrypoint for the command-line interface."""

import json
import sys
from pathlib import Path
from typing import NoReturn

import click
import deal
from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import prompts
from .constants import GPT_MODEL_DEFAULT
from .postprocessing import strlist_to_text, tldr_to_markdown, unfence
from .preprocessing import extract_subtitles, fetch_url, summarize
from .talk import talk
from .utils import get_input


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
    data = get_input()

    print(
        talk(
            prompt_system=prompts.vcard,
            data_user=data,
            model="gpt-3.5-turbo-16k",
            preprocessors=[fetch_url, summarize],
        )
    )

    sys.exit(0)


@cli.command()
def tldr() -> NoReturn:
    """Provide a tl;dr on a stream."""
    data = get_input()

    result = talk(
        prompt_system=prompts.tldr,
        data_user=data,
        model=GPT_MODEL_DEFAULT,
        preprocessors=[extract_subtitles, fetch_url, summarize],
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

    print(
        talk(
            prompt_system=prompts.subsfix,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
        )
    )

    sys.exit(0)


@cli.command()
def translate() -> NoReturn:
    """Translate some text."""
    data = get_input()

    print(
        talk(
            prompt_system=prompts.translate,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
        )
    )

    sys.exit(0)


@cli.command()
def explain() -> NoReturn:
    """Explain some code."""
    data = get_input()

    print(
        talk(
            prompt_system=prompts.explain,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
        )
    )

    sys.exit(0)


@cli.command()
def textwall() -> NoReturn:
    """Break up walls of text."""
    data = get_input()

    print(
        talk(
            prompt_system=prompts.textwall,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
            postprocessors=[unfence, strlist_to_text],
        )
    )

    sys.exit(0)


@cli.command()
def brief() -> NoReturn:
    """Write a case brief based on a legal ruling or opinion."""
    data = get_input()

    r = json.loads(
        talk(
            prompt_system=prompts.brief,
            data_user=data,
            model=GPT_MODEL_DEFAULT,
            preprocessors=[fetch_url],
            postprocessors=[unfence],
        ),
    )

    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("brief.md")

    print(
        template.render(
            citation=r["citation"],
            parties=r["parties"],
            facts=[
                item["data"]
                for item in r["narrative"]
                if item["type"] == "fact"
            ],
            prior_proceedings=[
                item["data"]
                for item in r["narrative"]
                if item["type"] == "prior_proceeding"
            ],
            issue=r["issue"],
            rule=r["rule"],
            application=r["application"],
            conclusion=r["conclusion"],
        )
    )

    sys.exit(0)
