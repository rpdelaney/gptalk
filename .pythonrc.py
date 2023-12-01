# flake8: noqa
try:
    from readability import Document

    from gptalk.utils import fetch_url, summarize
except Exception as exc:
    print(exc)
