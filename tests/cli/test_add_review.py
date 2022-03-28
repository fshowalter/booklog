from datetime import date
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.api import AuthorWithWorks, ProgressMark, Work, WorkAuthor
from booklog.cli import add_review
from tests.cli.conftest import MockInput
from tests.cli.keys import Backspace, Enter


@pytest.fixture(autouse=True)
def mock_create_review(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_review.booklog_api.create_review")


@pytest.fixture(autouse=True)
def mock_create_search_authors(mocker: MockerFixture) -> MagicMock:
    authors_with_works = [
        AuthorWithWorks(
            name="Stephen King",
            sort_name="King, Stephen",
            slug="stephen-king",
            works=[
                Work(
                    title="On Writing",
                    subtitle="A Memoir of the Craft",
                    year="2000",
                    sort_title="On Writing: A Memoir of the Craft",
                    authors=[WorkAuthor(slug="stephen-king", notes=None)],
                    slug="on-writing-by-stephen-king",
                    kind="Kindle",
                )
            ],
        )
    ]

    return mocker.patch(
        "booklog.cli.ask_for_author.booklog_api.search_authors",
        return_value=authors_with_works,
    )


@pytest.fixture(autouse=True)
def stub_editions(mocker: MockerFixture) -> None:
    editions = [
        "Kindle",
        "Audible",
        "Paperback",
        "Hardback",
    ]

    mocker.patch(
        "booklog.cli.add_review.booklog_api.all_editions", return_value=editions
    )


CLEAR_DEFAULT_DATE = "".join(
    [
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
)


def test_calls_add_review(mock_input: MockInput, mock_create_review: MagicMock) -> None:
    mock_input(
        [
            "Stephen King",
            Enter,
            Enter,
            "y",
            Enter,
            "y",
            CLEAR_DEFAULT_DATE,
            "2016-03-10",
            Enter,
            "y",
            "15",
            Enter,
            "y",
            CLEAR_DEFAULT_DATE,
            "2016-03-11",
            Enter,
            "y",
            "50",
            Enter,
            "y",
            CLEAR_DEFAULT_DATE,
            "2016-03-12",
            Enter,
            "y",
            "100",
            Enter,
            Enter,
            "y",
            "A+",
            Enter,
            "y",
        ]
    )

    add_review.prompt()

    mock_create_review.assert_called_once_with(
        work_slug="on-writing-by-stephen-king",
        edition="Kindle",
        progress=[
            ProgressMark(date=date(2016, 3, 10), percent=15),
            ProgressMark(date=date(2016, 3, 11), percent=50),
            ProgressMark(date=date(2016, 3, 12), percent=100),
        ],
        grade="A+",
    )
