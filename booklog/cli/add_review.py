from __future__ import annotations

import html
import re
from datetime import date, datetime
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator

from booklog.cli import ask, ask_for_work, radio_list
from booklog.data import api as data

Option = Tuple[Optional[str], AnyFormattedText]

WorkOption = Tuple[Optional[data.Work], AnyFormattedText]


def prompt() -> None:
    work_with_authors = ask_for_work.prompt()

    if not work_with_authors:
        return

    timeline = ask_for_timeline()

    if not timeline:
        return

    edition = ask_for_edition()

    if not edition:
        return

    grade = None

    if timeline[-1].progress == "Abandoned":
        grade = "Abandoned"
    else:
        grade = ask_for_grade()

    if not grade:
        return

    data.create_reading(
        work_slug=work_with_authors.slug,
        edition=edition,
        timeline=timeline,
    )

    data.create_review(
        work_slug=work_with_authors.slug,
        date=timeline[-1].date,
        grade=grade,
    )


def is_date(text: str) -> bool:
    try:
        return bool(string_to_date(text))
    except ValueError:
        return False


def string_to_date(date_string: str) -> date:
    return datetime.strptime(date_string, "%Y-%m-%d").date()  # noqa: WPS323


def ask_for_date(default_date: Optional[date] = None) -> Optional[date]:
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
        default=default_date.strftime("%Y-%m-%d"),  # noqa: WPS323
    )

    if not date_string:
        return None

    given_date = string_to_date(date_string)

    if confirm(given_date.strftime("%A, %B, %-d, %Y?")):  # noqa: WPS323
        return given_date

    return ask_for_date()


def is_valid_progress(text: str) -> bool:
    if text in {"F", "A"}:
        return True

    return bool(re.match("^[0-9]$|^[1-9][0-9]$|^(100)$", text))


def ask_for_progress() -> str:
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

        return "{0}%".format(progress)

    return ask_for_progress()


def ask_for_timeline() -> list[data.TimelineEntry]:
    timeline_entries: list[data.TimelineEntry] = []
    timeline_date = None

    while True:
        timeline_date = ask_for_date(timeline_date)

        if timeline_date:
            progress = ask_for_progress()

            timeline_entries.append(
                data.TimelineEntry(date=timeline_date, progress=progress)
            )

            if progress in {"Finished", "Abandoned"}:
                return timeline_entries


def ask_for_edition() -> Optional[str]:
    options: List[Option] = build_edition_options()

    selected_edition = None

    while selected_edition is None:
        selected_edition = radio_list.prompt(
            title="Select edition:",
            options=options,
        )

        selected_edition = selected_edition or new_edition()

        if selected_edition is None:
            break

    if not selected_edition:
        return None

    if confirm("{0}?".format(selected_edition)):
        return selected_edition

    return ask_for_edition()


def build_edition_options() -> List[Option]:
    editions = data.all_editions()

    options: list[Option] = []

    for edition in editions:
        option = (edition, "<cyan>{0}</cyan>".format(html.escape(edition)))
        options.append(option)

    options.append((None, "New edition"))

    return options


def new_edition() -> Optional[str]:
    return ask.prompt("Edition: ")


def is_grade(text: str) -> bool:
    return bool(re.match("[a-d|A-D|f|F][+|-]?", text))


def ask_for_grade() -> Optional[str]:
    validator = Validator.from_callable(
        is_grade,
        error_message="Must be a valid grade.",
        move_cursor_to_end=True,
    )

    review_grade = ask.prompt("Grade: ", validator=validator, default="")

    if not review_grade:
        return None

    if confirm(review_grade):  # noqa: WPS323
        return review_grade

    return ask_for_grade()
