# flake8: noqa
try:
    from gptalk.utils import fetch_url, summarize
    from readability import Document
except Exception as exc:
    print(exc)
