import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.cli import add_author
from tests.cli.conftest import MockInput
from tests.cli.keys import Enter, Escape


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture
def mock_create_author(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("booklog.cli.add_author.data_api.create_author")


def test_calls_create_author(
    mock_input: MockInput, mock_create_author: MagicMock
) -> None:
    mock_input(
        [
            "Stephen King",
            Enter,
            "y",
        ]
    )

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


def test_does_not_add_blank_author(
    mock_input: MockInput, mock_create_author: MagicMock
) -> None:
    mock_input(
        [
            Enter,
        ]
    )

    add_author.prompt()

    mock_create_author.assert_not_called()


def test_can_correct_input(
    mock_input: MockInput, mock_create_author: MagicMock
) -> None:
    mock_input(
        [
            "Steven Kang",
            Enter,
            "n",
            "Stephen King",
            Enter,
            "y",
        ]
    )

    add_author.prompt()

    mock_create_author.assert_called_once_with("Stephen King")


def test_can_create_author(
    mock_input: MockInput, tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    mock_input(
        [
            "Stephen King",
            Enter,
            "y",
        ]
    )

    add_author.prompt()

    with open(
        os.path.join(tmp_path / "authors" / "stephen-king.json"),
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
