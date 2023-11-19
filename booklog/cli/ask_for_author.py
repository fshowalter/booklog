from __future__ import annotations

import html
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, radio_list
from booklog.data import api as data_api

AuthorOption = Tuple[Optional[data_api.AuthorWithWorks], AnyFormattedText]


def prompt() -> Optional[data_api.AuthorWithWorks]:
    while True:
        name = ask.prompt("Author: ")

        if not name:
            return None

        authors = data_api.search_authors(name)

        options: list[AuthorOption] = build_author_options(authors)

        selected_author = None

        selected_author = radio_list.prompt(
            title="Select author:",
            options=options,
        )

        if selected_author:
            return selected_author


def build_author_options(
    authors: list[data_api.AuthorWithWorks],
) -> List[AuthorOption]:
    if not authors:
        return [(None, "Search Again")]

    return [
        (
            author,
            "<cyan>{0}</cyan> ({1})".format(
                html.escape(author.sort_name),
                ", ".join(html.escape(work.title) for work in author.works[:3]),
            ),
        )
        for author in authors
    ]
