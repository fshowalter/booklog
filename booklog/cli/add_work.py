from __future__ import annotations

import html
from typing import Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, ask_for_author, ask_for_work, radio_list
from booklog.data import api as data_api

AuthorOption = Tuple[Optional[data_api.AuthorWithWorks], AnyFormattedText]

Option = Tuple[Optional[str], AnyFormattedText]


def prompt() -> None:  # noqa: WPS210, WPS231
    works = []
    work_authors = ask_for_authors()

    if not work_authors:
        return

    while True:
        kind = ask_for_kind()

        if not kind:
            return

        title = ask_for_title()

        if not title:
            return

        subtitle = None

        if kind == "Nonfiction":
            subtitle = ask_for_subtitle()

        year = ask_for_year()

        if not year:
            return

        included_works = []

        if kind in {"Collection", "Anthology"}:
            included_works = ask_for_works()

        works.append(
            data_api.create_work(
                title=title,
                work_authors=work_authors,
                subtitle=subtitle,
                year=year,
                kind=kind,
                included_work_slugs=included_works,
            )
        )

        if not ask_to_add_more_works(work_authors):
            return


def ask_to_add_more_works(work_authors: list[data_api.WorkAuthor]) -> bool:
    work_author_names = " ".join(author.name() for author in work_authors)

    return confirm("Add more works by {0}?".format(work_author_names))


def ask_for_year() -> Optional[str]:
    year = ask.prompt("Year First Published: ")

    if not year:
        return None

    if confirm(year):  # noqa: WPS323
        return year

    return ask_for_year()


def ask_for_authors() -> list[data_api.CreateWorkAuthor]:
    work_authors: list[data_api.CreateWorkAuthor] = []

    while True:
        author = ask_for_author.prompt()

        if author:
            author_notes = ask.prompt("Notes: ")

            if not author_notes:
                author_notes = None

            work_authors.append(
                data_api.CreateWorkAuthor(slug=author.slug, notes=author_notes)
            )

        if not confirm("Add more Authors?"):
            return work_authors


def ask_for_works() -> list[str]:
    works: list[str] = []

    while True:
        work = ask_for_work.prompt()

        if work:
            works.append(work.slug)

        if not confirm("Add more?"):
            return works


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
    kinds = sorted(data_api.WORK_KINDS)

    options: list[Option] = []

    for kind in kinds:
        option = (kind, "<cyan>{0}</cyan>".format(html.escape(kind)))
        options.append(option)

    options.append((None, "Go back"))

    return options
