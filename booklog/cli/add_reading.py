from __future__ import annotations

import html
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Literal

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator

from booklog.cli import ask, radio_list, select_work
from booklog.repository import api as repository_api

Option = tuple[None | str, AnyFormattedText]

Stages = Literal[
    "ask_for_work",
    "ask_for_timeline",
    "ask_for_edition",
    "ask_for_grade",
    "persist_reading",
    "end",
]


@dataclass(kw_only=True)
class State:
    stage: Stages = "ask_for_work"
    work: repository_api.Work | None = None
    timeline: list[repository_api.TimelineEntry] = field(default_factory=list)
    edition: str | None = None
    grade: str | None = None


def prompt() -> None:
    state = State()

    state_machine: dict[Stages, Callable[[State], State]] = {
        "ask_for_work": ask_for_work,
        "ask_for_timeline": ask_for_timeline,
        "ask_for_edition": ask_for_edition,
        "ask_for_grade": ask_for_grade,
        "persist_reading": persist_reading,
    }

    while state.stage != "end":
        state_machine[state.stage](state)


def persist_reading(state: State) -> State:
    assert state.work
    assert state.edition
    assert state.timeline
    assert state.grade

    repository_api.create_reading(
        work=state.work,
        edition=state.edition,
        timeline=state.timeline,
    )

    repository_api.create_or_update_review(
        work=state.work, date=state.timeline[-1].date, grade=state.grade
    )

    if confirm("Add another reading?"):
        state.stage = "ask_for_work"
    else:
        state.stage = "end"

    return state


def ask_for_work(state: State) -> State:
    state.work = None

    work = select_work.prompt()

    if not work:
        state.stage = "end"
        return state

    state.work = work
    state.stage = "ask_for_timeline"
    return state


def is_date(text: str) -> bool:
    try:
        return bool(string_to_date(text))
    except ValueError:
        return False


def string_to_date(date_string: str) -> date:
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def ask_for_date(default_date: date | None = None) -> date | None:
    default_date = default_date or date.today()

    validator = Validator.from_callable(
        is_date,
        error_message="Must be a valid date in YYYY-MM-DD format.",
        move_cursor_to_end=True,
    )

    date_string = ask.prompt(
        "Date: ",
        rprompt="YYYY-MM-DD format.",
        validator=validator,
        default=default_date.strftime("%Y-%m-%d"),
    )

    if not date_string:
        return None

    return string_to_date(date_string)


def is_valid_progress(text: str) -> bool:
    if text in {"F", "A"}:
        return True

    return bool(re.match("^[0-9]$|^[1-9][0-9]$|^(100)$", text))


def ask_for_progress() -> str | None:
    validator = Validator.from_callable(
        is_valid_progress,
        error_message='Must be a whole number (no % sign), F for "Finished", or A for "Abandoned"',
        move_cursor_to_end=True,
    )

    progress = ask.prompt(
        "Progress: ",
        validator=validator,
        default="",
        rprompt='Whole number (no % sign), F for "Finished", or A for "Abandoned"',
    )

    if progress:
        if progress == "F":
            return "Finished"

        if progress == "A":
            return "Abandoned"

        return f"{progress}%"

    return progress


def ask_for_timeline(state: State) -> State:
    state.timeline = []
    timeline_date = None

    while True:
        timeline_date = ask_for_date(timeline_date)

        if not timeline_date and not state.timeline:
            state.stage = "ask_for_work"
            return state

        if timeline_date:
            progress = ask_for_progress()

            if not progress:
                continue

            state.timeline.append(
                repository_api.TimelineEntry(date=timeline_date, progress=progress)
            )

            if progress in {"Finished", "Abandoned"}:
                state.stage = "ask_for_edition"
                return state


def ask_for_edition(state: State) -> State:
    state.edition = None
    options = build_edition_options()

    selected_edition = None

    while selected_edition is None:
        selected_edition = radio_list.prompt(
            title="Select edition:",
            options=options,
        )

        selected_edition = selected_edition or ask.prompt("Edition: ")

        if selected_edition is None:
            break

    if not selected_edition:
        state.stage = "ask_for_timeline"
        return state

    state.edition = selected_edition
    state.stage = "ask_for_grade"

    return state


def build_edition_options() -> list[Option]:
    editions = repository_api.reading_editions()

    options: list[Option] = [
        (edition, f"<cyan>{html.escape(edition)}</cyan>") for edition in editions
    ]

    options.append((None, "New edition"))

    return options


def is_grade(text: str) -> bool:
    return bool(re.match("[a-d|A-D|f|F][+|-]?", text))


def ask_for_grade(state: State) -> State:
    state.grade = None

    if state.timeline[-1].progress == "Abandoned":
        state.grade = "Abandoned"
        state.stage = "persist_reading"
        return state

    validator = Validator.from_callable(
        is_grade,
        error_message="Must be a valid grade.",
        move_cursor_to_end=True,
    )

    review_grade = ask.prompt("Grade: ", validator=validator, default="")

    if not review_grade:
        state.stage = "ask_for_edition"
        return state

    state.grade = review_grade
    state.stage = "persist_reading"

    return state
