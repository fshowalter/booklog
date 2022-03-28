from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import main
from tests.cli.conftest import MockInput
from tests.cli.keys import ControlD, Down, Enter, Up


@pytest.fixture(autouse=True)
def mock_add_review(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.add_review.prompt")


@pytest.fixture(autouse=True)
def mock_manage_data(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.manage_data.prompt")


@pytest.fixture(autouse=True)
def mock_export_data(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.booklog_api.export_data")


def test_calls_manage_data(mock_input: MockInput, mock_manage_data: MagicMock) -> None:
    mock_input([Enter, ControlD])
    main.prompt()

    mock_manage_data.assert_called_once()


def test_calls_add_review(mock_input: MockInput, mock_add_review: MagicMock) -> None:
    mock_input([Down, Enter, ControlD])
    main.prompt()

    mock_add_review.assert_called_once()


def test_calls_export_data(
    mock_input: MockInput,
    mock_export_data: MagicMock,
) -> None:
    mock_input([Up, Up, Enter, "y", Up, Enter])
    main.prompt()

    mock_export_data.assert_called_once()
