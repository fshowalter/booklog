from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from booklog.cli import main
from tests.cli.conftest import MockInput
from tests.cli.keys import ControlD, Down, Enter, Up


@pytest.fixture(autouse=True)
def mock_add_reading(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.add_reading.prompt")


@pytest.fixture(autouse=True)
def mock_add_author(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.add_author.prompt")


@pytest.fixture(autouse=True)
def mock_add_title(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.add_title.prompt")


@pytest.fixture(autouse=True)
def mock_export_data(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.main.exports_api.export_data")


def test_calls_add_author(mock_input: MockInput, mock_add_author: MagicMock) -> None:
    mock_input([Enter, ControlD])
    main.prompt()

    mock_add_author.assert_called_once()


def test_calls_add_title(mock_input: MockInput, mock_add_title: MagicMock) -> None:
    mock_input([Down, Enter, ControlD])
    main.prompt()

    mock_add_title.assert_called_once()


def test_calls_add_reading(mock_input: MockInput, mock_add_reading: MagicMock) -> None:
    mock_input([Down, Down, Enter, ControlD])
    main.prompt()

    mock_add_reading.assert_called_once()


def test_can_export_data(mock_input: MockInput, mock_export_data: MagicMock) -> None:
    mock_input([Up, Enter, ControlD])
    main.prompt()

    mock_export_data.assert_called_once()
