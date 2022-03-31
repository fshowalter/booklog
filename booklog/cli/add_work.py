from __future__ import annotations

import html
from typing import Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog import api as booklog_api
from booklog.cli import ask, radio_list

AuthorOption = Tuple[Optional[booklog_api.AuthorWithWorks], AnyFormattedText]

Option = Tuple[Optional[str], AnyFormattedText]


def prompt() -> None:
    kind = ask_for_kind()

    if not kind:
        return

    title = ask_for_title()

    if not title:
        return

    subtitle = ask_for_subtitle()

    year = ask_for_year()

    if not year:
        return

    work_authors = ask_for_authors()

    if not work_authors:
        return

    booklog_api.create_work(
        title=title,
        authors=work_authors,
        subtitle=subtitle,
        year=year,
        kind=kind,
    )


def ask_for_year() -> Optional[str]:
    year = ask.prompt("Year First Published: ")

    if not year:
        return None

    if confirm(year):  # noqa: WPS323
        return year

    return ask_for_year()


def ask_for_authors() -> list[booklog_api.WorkAuthor]:
    work_authors: list[booklog_api.WorkAuthor] = []

    while True:
        author_slug = ask_for_author()

        if author_slug:
            author_notes = ask.prompt("Notes: ")

            if not author_notes:
                author_notes = None

            work_authors.append(
                booklog_api.WorkAuthor(slug=author_slug, notes=author_notes)
            )

        if not confirm("Add more?"):
            return work_authors


def ask_for_author() -> Optional[str]:
    name = None

    while name is None:
        name = ask.prompt("Author name: ")

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
        return selected_author.slug

    return ask_for_author()


def build_author_options(
    authors: list[booklog_api.AuthorWithWorks],
) -> list[AuthorOption]:
    options: list[AuthorOption] = []

    for author in authors:
        option = (
            author,
            "<cyan>{0}</cyan> ({1})".format(
                html.escape(author.sort_name),
                ", ".join(html.escape(work.title) for work in author.works),
            ),
        )
        options.append(option)

    options.append((None, "Search again"))

    return options


def ask_for_title() -> Optional[str]:
    title = ask.prompt("Title: ")

    if not title:
        return None

    if confirm(title):  # noqa: WPS323
        return title

    return ask_for_title()


def ask_for_subtitle() -> Optional[str]:
    subtitle = ask.prompt("Sub-title: ")

    if not subtitle:
        return None

    if confirm(subtitle):  # noqa: WPS323
        return subtitle

    return ask_for_subtitle()


def ask_for_kind() -> Optional[str]:
    options: list[Option] = build_kind_options()

    selected_kind = None

    while selected_kind is None:

        selected_kind = radio_list.prompt(
            title="Select kind:",
            options=options,
        )

        if selected_kind is None:
            break

    return selected_kind


def build_kind_options() -> list[Option]:
    kinds = booklog_api.WORK_KINDS

    options: list[Option] = []

    for kind in kinds:
        option = (kind, "<cyan>{0}</cyan>".format(html.escape(kind)))
        options.append(option)

    options.append((None, "Go back"))

    return options
