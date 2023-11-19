import json
import os
from pathlib import Path
from typing import Optional
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
def created_author() -> data_api.Author:
    return data_api.create_author("Richard Laymon")


def enter_author(name: str = "Laymon") -> list[str]:
    return [name, Enter]


def select_author_search_result() -> list[str]:
    return [Enter]


def enter_notes(notes: Optional[str] = None) -> list[str]:
    if notes:
        return [notes, Enter]

    return [Enter]


def select_kind_novel() -> list[str]:
    return [
        Down,
        Down,
        Down,
        Enter,
    ]


def enter_title(title: str) -> list[str]:
    return [title, Enter]


def enter_year_published(year: str) -> list[str]:
    return [year, Enter]


def test_calls_create_work(
    mock_input: MockInput, created_author: data_api.Author, mock_create_work: MagicMock
) -> None:
    mock_input(
        [
            *enter_author(created_author.name[:6]),
            *select_author_search_result(),
            *enter_notes(),
            "n",
            *select_kind_novel(),
            *enter_title("The Cellar"),
            "y",
            *enter_year_published("1980"),
            "n",
        ]
    )

    add_work.prompt()

    mock_create_work.assert_called_once_with(
        title="The Cellar",
        subtitle=None,
        work_authors=[
            data_api.WorkAuthor(
                name=created_author.name,
                sort_name=created_author.sort_name,
                notes=None,
                slug=created_author.slug,
            )
        ],
        year="1980",
        kind="Novel",
        included_work_slugs=[],
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


def test_can_create_work(
    mock_input: MockInput,
    created_author: data_api.Author,
    tmp_path: Path,
    snapshot_json: SnapshotAssertion,
) -> None:
    mock_input(
        [
            *enter_author(created_author.name[:6]),
            *select_author_search_result(),
            *enter_notes(),
            "n",
            *select_kind_novel(),
            *enter_title("The Cellar"),
            "y",
            *enter_year_published("1980"),
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
