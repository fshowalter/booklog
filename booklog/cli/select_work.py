from __future__ import annotations

import html
from typing import Iterable, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, radio_list
from booklog.cli.utils.array_to_sentence import array_to_sentence
from booklog.repository import api as repository_api

WorkOption = Tuple[Optional[repository_api.Work], AnyFormattedText]


def prompt() -> Optional[repository_api.Work]:
    while True:
        title = ask.prompt("Title: ")

        if title is None:
            return None

        works = search_works(title)
        options = build_work_options(works)

        selected_work = radio_list.prompt(
            title="Select work:",
            options=options,
        )

        if selected_work is None:
            continue

        if confirm("{0}?".format(selected_work.title)):
            return selected_work


def search_works(query: str) -> list[repository_api.Work]:
    return list(
        filter(
            lambda work: query.lower()
            in "{0}: {1}".format(work.title, work.subtitle).lower(),
            repository_api.works(),
        )
    )


def build_work_options(
    works: Iterable[repository_api.Work],
) -> list[WorkOption]:
    if not works:
        return [(None, "Search Again")]

    return [
        (
            work,
            "<cyan>{0}</cyan> by {1}".format(
                html.escape(work.title),
                array_to_sentence(
                    [
                        html.escape(work_author.author().name)
                        for work_author in work.work_authors
                    ]
                ),
            ),
        )
        for work in works
    ]
