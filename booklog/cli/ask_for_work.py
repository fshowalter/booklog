from __future__ import annotations

import html
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog import api as booklog_api
from booklog.cli import ask, radio_list

WorkOption = Tuple[Optional[booklog_api.WorkWithAuthors], AnyFormattedText]


def prompt() -> Optional[booklog_api.WorkWithAuthors]:
    title = None

    while title is None:
        title = ask.prompt("Title: ")

    works = booklog_api.search_works(title)

    options: list[WorkOption] = build_work_options(works)

    selected_work = None

    while selected_work is None:

        selected_work = radio_list.prompt(
            title="Select work:",
            options=options,
        )

        if selected_work is None:
            break

    if not selected_work:
        return None

    if confirm("{0}?".format(selected_work.title)):
        return selected_work

    return prompt()


def build_work_options(
    works: list[booklog_api.WorkWithAuthors],
) -> List[WorkOption]:
    options: list[WorkOption] = []

    for work in works:
        option = (
            work,
            "<cyan>{0}</cyan> by {1}".format(
                html.escape(work.title),
                ", ".join(
                    html.escape(author_name) for author_name in work.author_names
                ),
            ),
        )

        options.append(option)

    options.append((None, "Search again"))

    return options
