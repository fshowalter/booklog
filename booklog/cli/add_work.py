from __future__ import annotations

import html
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask, radio_list, select_author, select_work
from booklog.cli.utils.array_to_sentence import array_to_sentence
from booklog.repository import api as repository_api

Stages = Literal[
    "ask_for_authors",
    "ask_for_kind",
    "ask_for_title",
    "ask_for_subtitle",
    "ask_for_year",
    "ask_for_included_works",
    "persist_work",
    "end",
]


@dataclass(kw_only=True)
class State:
    stage: Stages = "ask_for_authors"
    kind: repository_api.Kind | None = None
    title: str | None = None
    work_authors: list[repository_api.WorkAuthor] = field(default_factory=list)
    subtitle: str | None = None
    year_published: str | None = None
    included_works: list[str] = field(default_factory=list)


def prompt() -> None:
    state = State()

    state_machine: dict[Stages, Callable[[State], State]] = {
        "ask_for_authors": ask_for_authors,
        "ask_for_kind": ask_for_kind,
        "ask_for_title": ask_for_title,
        "ask_for_subtitle": ask_for_subtitle,
        "ask_for_year": ask_for_year,
        "ask_for_included_works": ask_for_included_works,
        "persist_work": persist_work,
    }

    while state.stage != "end":
        state_machine[state.stage](state)


def persist_work(state: State) -> State:
    assert state.year_published
    assert state.title
    assert state.kind
    assert state.work_authors

    repository_api.create_work(
        title=state.title,
        work_authors=state.work_authors,
        subtitle=state.subtitle,
        year=state.year_published,
        kind=state.kind,
        included_work_slugs=state.included_works,
    )

    author_names = array_to_sentence([
        found_author.name if (found_author := author.author()) else author.author_slug
        for author in state.work_authors
    ])

    if confirm(f"Add more works by {author_names}?"):
        state.stage = "ask_for_kind"
    else:
        state.stage = "end"

    return state


def ask_for_year(state: State) -> State:
    state.year_published = None

    year = ask.prompt("Year First Published: ")

    if not year:
        state.stage = "ask_for_subtitle"
        return state

    state.year_published = year
    state.stage = "ask_for_included_works"
    return state


def ask_for_authors(state: State) -> State:
    state.work_authors = []

    while True:
        author = select_author.prompt()

        if not author:
            state.stage = "end"
            return state

        author_notes = ask.prompt("Notes: ")

        if author_notes is None:
            continue

        if author_notes == "":
            author_notes = None

        state.work_authors.append(
            repository_api.WorkAuthor(notes=author_notes, author_slug=author.slug)
        )

        if not confirm("Add more Authors?"):
            state.stage = "ask_for_kind"
            return state


def ask_for_included_works(state: State) -> State:
    state.included_works = []

    if state.kind not in {"Collection", "Anthology"}:
        state.stage = "persist_work"
        return state

    while True:
        work = select_work.prompt()

        if not work and not state.included_works:
            state.stage = "ask_for_year"
            return state

        if work:
            state.included_works.append(work.slug)

        if confirm("Add more?"):
            continue

        state.stage = "persist_work"
        return state


def ask_for_title(state: State) -> State:
    state.title = None
    title = ask.prompt("Title: ")

    if not title:
        state.stage = "ask_for_kind"
        return state

    if confirm(title):
        state.title = title
        state.stage = "ask_for_subtitle"

    return state


def ask_for_subtitle(state: State) -> State:
    state.subtitle = None

    if state.kind != "Nonfiction":
        state.stage = "ask_for_year"
        return state

    subtitle = ask.prompt("Sub-title: ")

    if subtitle is None:
        state.stage = "ask_for_title"
        return state

    if confirm(subtitle):
        state.subtitle = subtitle if subtitle else None
        state.stage = "ask_for_year"

    return state


def ask_for_kind(state: State) -> State:
    state.kind = None

    kind = radio_list.prompt(
        title="Select kind:",
        options=[
            (kind, f"<cyan>{html.escape(kind)}</cyan>")
            for kind in sorted(repository_api.WORK_KINDS)
        ],
    )

    if not kind:
        state.stage = "ask_for_authors"
        return state

    state.kind = kind
    state.stage = "ask_for_title"

    return state
