from __future__ import annotations

import html
import re
from datetime import date, datetime
from typing import List, Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator

from booklog import api as booklog_api
from booklog.cli import ask, ask_for_author, radio_list

Option = Tuple[Optional[str], AnyFormattedText]

WorkOption = Tuple[Optional[booklog_api.Work], AnyFormattedText]


def prompt() -> None:
    work_slug = ask_for_work()

    if not work_slug:
        return

    progress = ask_for_progress()

    if not progress:
        return

    edition = ask_for_edition()

    if not edition:
        return

    grade = ask_for_grade()

    if not grade:
        return

    booklog_api.create_review(
        work_slug=work_slug,
        edition=edition,
        progress=progress,
        grade=grade,
    )


def is_date(text: str) -> bool:
    try:
        return bool(string_to_date(text))
    except ValueError:
        return False


def string_to_date(date_string: str) -> date:
    return datetime.strptime(date_string, "%Y-%m-%d").date()  # noqa: WPS323


def ask_for_date() -> Optional[date]:
    validator = Validator.from_callable(
        is_date,
        error_message="Must be a valid date in YYYY-MM-DD format.",
        move_cursor_to_end=True,
    )

    date_string = ask.prompt(
        "Date: ",
        rprompt="YYYY-MM-DD format.",
        validator=validator,
        default=date.today().strftime("%Y-%m-%d"),  # noqa: WPS323
    )

    if not date_string:
        return None

    given_date = string_to_date(date_string)

    if confirm(given_date.strftime("%A, %B, %-d, %Y?")):  # noqa: WPS323
        return given_date

    return ask_for_date()


def is_percent(text: str) -> bool:
    return bool(re.match("^[0-9]$|^[1-9][0-9]$|^(100)$", text))


def ask_for_percent() -> int:
    validator = Validator.from_callable(
        is_percent,
        error_message="Must be a whole number (no % sign).",
        move_cursor_to_end=True,
    )

    percent = ask.prompt("Percent: ", validator=validator, default="")

    if percent:
        return int(percent)

    return ask_for_percent()


def ask_for_progress() -> list[booklog_api.ProgressMark]:
    progress_marks: list[booklog_api.ProgressMark] = []

    while True:
        progress_date = ask_for_date()

        if progress_date:
            progress_percent = ask_for_percent()

            progress_marks.append(
                booklog_api.ProgressMark(date=progress_date, percent=progress_percent)
            )

            if progress_percent == 100:
                return progress_marks

        if not confirm("Add more?"):
            return progress_marks


def ask_for_work() -> Optional[str]:
    author_with_works = ask_for_author.prompt()

    if not author_with_works:
        return None

    options: list[WorkOption] = build_work_options(author_with_works.works)

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
        return selected_work.slug

    return ask_for_work()


def build_work_options(
    works: list[booklog_api.Work],
) -> List[WorkOption]:
    options: list[WorkOption] = []

    for work in works:
        option = (
            work,
            "<cyan>{0}</cyan>".format(
                html.escape(work.full_title),
            ),
        )
        options.append(option)

    options.append((None, "Select another author"))

    return options


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
    editions = booklog_api.all_editions()

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
