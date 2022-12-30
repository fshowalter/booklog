from __future__ import annotations

from booklog import api as booklog_api
from booklog.cli import ask_for_author


def prompt() -> None:  # noqa: WPS210
    author = ask_for_author.prompt()

    if not author:
        return

    booklog_api.add_author_to_shelf(author_slug=author.slug)
