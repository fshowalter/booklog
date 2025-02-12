from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import add_author
from tests.cli.conftest import MockInput
from tests.cli.keys import Enter, Escape
from tests.cli.prompt_utils import enter_text


@pytest.fixture
def mock_create_author(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_author.repository_api.create_author")


def test_calls_create_author(mock_input: MockInput, mock_create_author: MagicMock) -> None:
    mock_input(enter_text("Stephen King", confirm="y"))

    add_author.prompt()

    mock_create_author.assert_called_once_with("Stephen King")


def test_can_cancel_out(mock_input: MockInput, mock_create_author: MagicMock) -> None:
    mock_input(
        [
            Escape,
        ]
    )

    add_author.prompt()

    mock_create_author.assert_not_called()


def test_does_not_add_blank_author(mock_input: MockInput, mock_create_author: MagicMock) -> None:
    mock_input(
        [
            Enter,
        ]
    )

    add_author.prompt()

    mock_create_author.assert_not_called()


def test_can_correct_input(mock_input: MockInput, mock_create_author: MagicMock) -> None:
    mock_input(
        [
            *enter_text("Steven Kang", confirm="n"),
            *enter_text("Stephen King", confirm="y"),
        ]
    )

    add_author.prompt()

    mock_create_author.assert_called_once_with("Stephen King")
