from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import add_work
from booklog.repository import api as repository_api
from tests.cli.conftest import MockInput
from tests.cli.keys import Escape
from tests.cli.prompt_utils import ConfirmType, enter_text, select_option


@pytest.fixture
def mock_create_work(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_work.repository_api.create_work")


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


def enter_author(name: str) -> list[str]:
    return enter_text(name)


def select_author_search_result() -> list[str]:
    return select_option(1)


def enter_notes(notes: str | None = None) -> list[str]:
    return enter_text(notes)


def select_kind_novel() -> list[str]:
    return select_option(4)


def select_kind_collection() -> list[str]:
    return select_option(2)


def select_title_search_result(confirm: ConfirmType) -> list[str]:
    return select_option(1, confirm=confirm)


def enter_title(title: str, confirm: ConfirmType) -> list[str]:
    return enter_text(title, confirm=confirm)


def enter_included_work_title(title: str) -> list[str]:
    return enter_text(title)


def enter_year_published(year: str) -> list[str]:
    return enter_text(year)


def test_calls_create_work(
    mock_input: MockInput,
    author_fixture: repository_api.Author,
    mock_create_work: MagicMock,
) -> None:
    mock_input(
        [
            *enter_author(author_fixture.name[:6]),
            *select_author_search_result(),
            *enter_notes(),
            "n",
            *select_kind_novel(),
            *enter_title("The Cellar", confirm="y"),
            *enter_year_published("1980"),
            "n",
        ]
    )

    add_work.prompt()

    mock_create_work.assert_called_once_with(
        title="The Cellar",
        subtitle=None,
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ],
        year="1980",
        kind="Novel",
        included_work_slugs=[],
    )


def test_calls_create_work_for_collection(
    mock_input: MockInput,
    author_fixture: repository_api.Author,
    mock_create_work: MagicMock,
    work_fixture: repository_api.Work,
) -> None:
    mock_input(
        [
            *enter_author(author_fixture.name[:6]),
            *select_author_search_result(),
            *enter_notes(),
            "n",
            *select_kind_collection(),
            *enter_title("The Richard Laymon Collection Volume 1", confirm="y"),
            *enter_year_published("2006"),
            *enter_included_work_title(work_fixture.title),
            *select_title_search_result("y"),
            "n",
            "n",
        ]
    )

    add_work.prompt()

    mock_create_work.assert_called_once_with(
        title="The Richard Laymon Collection Volume 1",
        subtitle=None,
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ],
        year="2006",
        kind="Collection",
        included_work_slugs=[work_fixture.slug],
    )


def test_can_cancel_out_of_author_name(
    mock_input: MockInput, mock_create_work: MagicMock
) -> None:
    mock_input(
        [
            Escape,
        ]
    )

    add_work.prompt()

    mock_create_work.assert_not_called()


def test_can_cancel_out_of_kind(
    mock_input: MockInput, mock_create_work: MagicMock
) -> None:
    mock_input(
        [
            Escape,
        ]
    )

    add_work.prompt()

    mock_create_work.assert_not_called()
