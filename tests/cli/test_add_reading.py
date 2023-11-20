from datetime import date
from typing import Optional
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import add_reading
from booklog.data import api as data_api
from booklog.data.api import TimelineEntry
from tests.cli.conftest import MockInput
from tests.cli.keys import Backspace, Down, Enter


@pytest.fixture
def mock_create_reading(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_reading.data_api.create_reading")


@pytest.fixture(autouse=True)
def created_author() -> data_api.Author:
    return data_api.create_author("Richard Laymon")


@pytest.fixture(autouse=True)
def created_work(created_author: data_api.Author) -> data_api.Work:
    return data_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_work_slugs=[],
        work_authors=[
            data_api.WorkAuthor(
                name=created_author.name,
                sort_name=created_author.sort_name,
                slug=created_author.slug,
                notes=None,
            )
        ],
    )


@pytest.fixture(autouse=True)
def stub_editions(mocker: MockerFixture) -> None:
    editions = [
        "Audible",
        "Hardback",
        "Kindle",
        "Paperback",
    ]

    mocker.patch("booklog.cli.add_reading.data_api.all_editions", return_value=editions)


def clear_default_date() -> list[str]:
    return [
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
        Backspace,
    ]


def enter_title(title: str = "Cellar") -> list[str]:
    return [title, Enter]


def select_title_search_result() -> list[str]:
    return [Enter]


def enter_notes(notes: Optional[str] = None) -> list[str]:
    if notes:
        return [notes, Enter]

    return [Enter]


def select_edition_kindle() -> list[str]:
    return [
        Down,
        Down,
        Enter,
    ]


def enter_date(date: str) -> list[str]:
    return [date, Enter]


def enter_progress(progress: str) -> list[str]:
    return [progress, Enter]


def enter_grade(grade: str) -> list[str]:
    return [grade, Enter]


def test_calls_add_reading(
    mock_input: MockInput, mock_create_reading: MagicMock, created_work: data_api.Work
) -> None:
    mock_input(
        [
            *enter_title(),
            *select_title_search_result(),
            "y",
            *clear_default_date(),
            *enter_date("2016-03-10"),
            "y",
            *enter_progress("15"),
            *clear_default_date(),
            *enter_date("2016-03-11"),
            "y",
            *enter_progress("50"),
            *clear_default_date(),
            *enter_date("2016-03-12"),
            "y",
            *enter_progress("F"),
            *select_edition_kindle(),
            "y",
            *enter_grade("A+"),
            "y",
            "n",
        ]
    )

    add_reading.prompt()

    mock_create_reading.assert_called_once_with(
        work_slug=created_work.slug,
        edition="Kindle",
        timeline=[
            TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
        grade="A+",
    )
