from __future__ import annotations

import html
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, radio_list
from booklog.cli.utils.array_to_sentence import array_to_sentence
from booklog.data import api as data_api

WorkOption = Tuple[Optional[data_api.Work], AnyFormattedText]


def prompt() -> Optional[data_api.Work]:
    while True:
        title = ask.prompt("Title: ")

        if title is None:
            return None

        works = data_api.search_works(title)

        options = build_work_options(works)

        selected_work = radio_list.prompt(
            title="Select work:",
            options=options,
        )

        if selected_work is None:
            continue

        if confirm("{0}?".format(selected_work.title)):
            return selected_work


def build_work_options(
    works: list[data_api.Work],
) -> List[WorkOption]:
    if not works:
        return [(None, "Search Again")]

    return [
        (
            work,
            "<cyan>{0}</cyan> by {1}".format(
                html.escape(work.title),
                array_to_sentence(
                    [html.escape(author.name) for author in work.authors]
                ),
            ),
        )
        for work in works
    ]
