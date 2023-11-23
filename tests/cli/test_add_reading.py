from datetime import date
from typing import Optional
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import add_reading
from booklog.repository import api as repository_api
from tests.cli.conftest import MockInput
from tests.cli.keys import Backspace, Down, Enter


@pytest.fixture
def mock_create_reading(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_reading.repository_api.create_reading")


@pytest.fixture
def mock_create_review(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "booklog.cli.add_reading.repository_api.create_or_update_review"
    )


@pytest.fixture(autouse=True)
def author_fixture() -> repository_api.Author:
    return repository_api.create_author("Richard Laymon")


@pytest.fixture(autouse=True)
def work_fixture(author_fixture: repository_api.Author) -> repository_api.Work:
    return repository_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_work_slugs=[],
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author_fixture.slug,
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

    mocker.patch(
        "booklog.cli.add_reading.repository_api.reading_editions", return_value=editions
    )


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


def test_calls_add_reading_and_add_review(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title(),
            *select_title_search_result(),
            "y",
            *clear_default_date(),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *clear_default_date(),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *clear_default_date(),
            *enter_date("2016-03-12"),
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
        work=work_fixture,
        edition="Kindle",
        timeline=[
            repository_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            repository_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            repository_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )

    mock_create_review.assert_called_once_with(
        work=work_fixture, grade="A+", date=date(2016, 3, 12)
    )
