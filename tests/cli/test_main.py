from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from booklog.cli import main
from tests.cli.conftest import MockInput
from tests.cli.keys import ControlD, Down, Enter, Up


@pytest.fixture(autouse=True)
def mock_add_reading(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    m = MagicMock()
    monkeypatch.setattr("booklog.cli.add_reading.prompt", m)
    return m


@pytest.fixture(autouse=True)
def mock_add_author(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    m = MagicMock()
    monkeypatch.setattr("booklog.cli.add_author.prompt", m)
    return m


@pytest.fixture(autouse=True)
def mock_add_title(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    m = MagicMock()
    monkeypatch.setattr("booklog.cli.add_title.prompt", m)
    return m


@pytest.fixture(autouse=True)
def mock_export_data(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    m = MagicMock()
    monkeypatch.setattr("booklog.exports.api.export_data", m)
    return m


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
