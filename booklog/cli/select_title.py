from __future__ import annotations

import html
from collections.abc import Iterable

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, radio_list
from booklog.cli.utils.array_to_sentence import array_to_sentence
from booklog.repository import api as repository_api

TitleOption = tuple[repository_api.Title | None, AnyFormattedText]


def prompt() -> repository_api.Title | None:
    while True:
        title = ask.prompt("Title: ")

        if title is None:
            return None

        titles = search_titles(title)
        options = build_title_options(titles)

        selected_title = radio_list.prompt(
            title="Select title:",
            options=options,
        )

        if selected_title is None:
            continue

        if confirm(f"{selected_title.title}?"):
            return selected_title


def search_titles(query: str) -> list[repository_api.Title]:
    return list(
        filter(
            lambda title: query.lower() in f"{title.title}: {title.subtitle}".lower(),
            repository_api.titles(),
        )
    )


def build_title_options(
    titles: Iterable[repository_api.Title],
) -> list[TitleOption]:
    if not titles:
        return [(None, "Search Again")]

    return [
        (
            title,
            "<cyan>{}</cyan> by {}".format(
                html.escape(title.title),
                array_to_sentence(
                    [
                        html.escape(title_author.author().name)
                        for title_author in title.title_authors
                    ]
                ),
            ),
        )
        for title in titles
    ]
