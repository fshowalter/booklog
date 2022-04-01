from __future__ import annotations

import html
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog import api as booklog_api
from booklog.cli import ask, radio_list

AuthorOption = Tuple[Optional[booklog_api.AuthorWithWorks], AnyFormattedText]


def prompt() -> Optional[booklog_api.AuthorWithWorks]:
    name = None

    while name is None:
        name = ask.prompt("Author: ")

    authors = booklog_api.search_authors(name)

    options: list[AuthorOption] = build_author_options(authors)

    selected_author = None

    while selected_author is None:

        selected_author = radio_list.prompt(
            title="Select author:",
            options=options,
        )

        if selected_author is None:
            break

    if not selected_author:
        return None

    if confirm("{0}?".format(selected_author.name)):
        return selected_author

    return prompt()


def build_author_options(
    authors: list[booklog_api.AuthorWithWorks],
) -> List[AuthorOption]:
    options: list[AuthorOption] = []

    for author in authors:
        works = author.works[:3]
        option = (
            author,
            "<cyan>{0}</cyan> ({1})".format(
                html.escape(author.sort_name),
                ", ".join(html.escape(work.title) for work in works),
            ),
        )
        options.append(option)

    options.append((None, "Search again"))

    return options
