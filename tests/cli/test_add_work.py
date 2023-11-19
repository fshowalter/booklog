import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.cli import add_work
from booklog.data import api as data_api
from tests.cli.conftest import MockInput
from tests.cli.keys import Down, Enter, Escape


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture
def mock_create_work(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_work.data_api.create_work")


@pytest.fixture(autouse=True)
def create_author() -> None:
    data_api.create_author("Richard Laymon")


def test_calls_create_work(mock_input: MockInput, mock_create_work: MagicMock) -> None:
    mock_input(
        [
            "Laymon",
            Enter,
            Enter,
            "y",
            "Editor",
            "n",
            Down,
            Enter,
            "Bad News",
            "y",
            "2000",
            "y",
            "n",
        ]
    )

    add_work.prompt()

    mock_create_work.assert_called_once_with("Stephen King")


def test_can_cancel_out(mock_input: MockInput, mock_create_work: MagicMock) -> None:
    mock_input(
        [
            Escape,
        ]
    )

    add_work.prompt()

    mock_create_work.assert_not_called()


def test_can_create_work(
    mock_input: MockInput, tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    mock_input(
        [
            "Laymon",
            Enter,
            Enter,
            "y",
            Enter,
            Enter,
            "n",
            Down,
            Down,
            Down,
            Enter,
            "The CellAr",
            Enter,
            "y",
            "1980",
            Enter,
            "y",
            "n",
        ]
    )

    add_work.prompt()

    with open(
        os.path.join(tmp_path / "works" / "the-cellar-by-richard-laymon.json"),
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
