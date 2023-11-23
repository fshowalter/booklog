from datetime import date
from typing import Optional
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import add_reading
from booklog.repository import api as repository_api
from tests.cli.conftest import MockInput
from tests.cli.keys import Backspace, Escape
from tests.cli.prompt_utils import ConfirmType, enter_text, select_option


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


def enter_title(title: str) -> list[str]:
    return enter_text(title)


def select_title_search_result(confirm: ConfirmType) -> list[str]:
    return select_option(1, confirm=confirm)


def select_search_again() -> list[str]:
    return select_option(1)


def enter_notes(notes: Optional[str] = None) -> list[str]:
    return enter_text(notes)


def select_edition_kindle() -> list[str]:
    return select_option(3)


def enter_date(date: str) -> list[str]:
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
        *enter_text(date),
    ]


def enter_progress(progress: str) -> list[str]:
    return enter_text(progress)


def enter_grade(grade: str) -> list[str]:
    return enter_text(grade)


def test_calls_add_reading_and_add_review(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
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


def test_can_search_again(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title("The Typo"),
            *select_search_again(),
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
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


def test_can_escape_from_first_date(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            Escape,
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
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


def test_can_escape_from_second_progress_and_date(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            Escape,
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2017-03-11"),
            Escape,
            Escape,
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
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


def test_can_escape_from_progress(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2015-03-11"),
            Escape,
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
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


def test_can_escape_from_title(
    mock_input: MockInput,
    mock_create_reading: MagicMock,
    mock_create_review: MagicMock,
) -> None:
    mock_input(
        [
            Escape,
        ]
    )

    add_reading.prompt()

    mock_create_reading.assert_not_called()

    mock_create_review.assert_not_called()
