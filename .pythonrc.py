# flake8: noqa
try:
    from readability import Document  # type: ignore[import-untyped]

    from gptalk.preprocessing import fetch_url, summarize
except Exception as exc:
    print(exc)
