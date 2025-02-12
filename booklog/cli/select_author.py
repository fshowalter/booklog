from __future__ import annotations

import html
import itertools
from collections.abc import Iterable

from prompt_toolkit.formatted_text import AnyFormattedText

from booklog.cli import ask, radio_list
from booklog.repository import api as repository_api

AuthorOption = tuple[repository_api.Author | None, AnyFormattedText]


def prompt() -> repository_api.Author | None:
    while True:
        name = ask.prompt("Author: ")

        if not name:
            return None

        authors = search_authors(name)

        options: list[AuthorOption] = build_author_options(authors)

        selected_author = None

        selected_author = radio_list.prompt(
            title="Select author:",
            options=options,
        )

        if selected_author:
            return selected_author


def search_authors(query: str) -> Iterable[repository_api.Author]:
    return filter(
        lambda author: query.lower() in author.name.lower(),
        repository_api.authors(),
    )


def format_author_works(author: repository_api.Author) -> str:
    first_three_author_works = itertools.islice(author.works(), 3)

    return ", ".join(html.escape(work.title) for work in first_three_author_works)


def build_author_options(
    authors: Iterable[repository_api.Author],
) -> list[AuthorOption]:
    if not authors:
        return [(None, "Search Again")]

    return [
        (
            author,
            f"<cyan>{html.escape(author.sort_name)}</cyan> ({format_author_works(author)})",
        )
        for author in authors
    ]
