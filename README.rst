GPTalk
======

``gptalk`` is a command-line grab bag of workflows I often use with LLMs.
`ChatGPT <https://chat.openai.com/>`__ is the only supported back-end.

Demo
----
GPTalk's commands can perform pre-processing. For example, if asked to summarize
a YouTube video, it will quietly extract the subtitles to the video and print a
summary:

|asciicast|

.. |asciicast| image:: https://asciinema.org/a/UDieN0MgIUfBBJluaiKl4aY8z.svg
   :target: https://asciinema.org/a/UDieN0MgIUfBBJluaiKl4aY8z

Installation
------------

I recommend `pipx <https://pipx.pypa.io/stable/>`__ for managing python
modules in your interactive shell.

.. code:: console

   $ poetry build && pipx install .

Usage
-----

.. code:: console

   $ gptalk --help
   Usage: gptalk [OPTIONS] COMMAND [ARGS]...

     Do some stuff with ChatGPT.

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     howdoi   Like `howdoi` but ChatGPT instead of StackOverflow.
     outline  Generate MECE outline of an arbitrary topic.
     subsfix  Fix subtitles generated with speech to text.
     ticket   Create a task ticket using a basic WHAT/WHY/AC format.
     tldr     Provide a tl;dr on a stream.
     vcard    Read unstructured data and output a contact card (VCF).

``gptalk`` has various subcommands. Data will is from standard input; if
not found, your $EDITOR will be opened.

Development
-----------

To install development dependencies, you will need ``poetry`` and
``pre-commit``:

.. code:: console

   $ pipx install poetry pre-commit
   [...]
   $ cd gptalk
   $ pre-commit install --install-hooks
   [...]
   $ poetry install && poetry shell
