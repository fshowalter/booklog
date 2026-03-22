from __future__ import annotations

import json
from pathlib import Path

import pytest

from booklog.cli import add_title
from booklog.repository import api as repository_api
from booklog.repository.types import NonEmptyList
from tests.cli.conftest import MockInput
from tests.cli.keys import Escape
from tests.cli.prompt_utils import ConfirmType, enter_text, select_option


@pytest.fixture(autouse=True)
def author_fixture() -> repository_api.Author:
    return repository_api.create_author("Richard Laymon")


@pytest.fixture(autouse=True)
def title_fixture(author_fixture: repository_api.Author) -> repository_api.Title:
    return repository_api.create_title(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_title_ids=[],
        title_authors=NonEmptyList(
            repository_api.TitleAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ),
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


def enter_included_title_text(title: str) -> list[str]:
    return enter_text(title)


def enter_year_published(year: str) -> list[str]:
    return enter_text(year)


def test_creates_title(
    mock_input: MockInput,
    author_fixture: repository_api.Author,
    tmp_path: Path,
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

    add_title.prompt()

    data = json.loads((tmp_path / "titles" / "the-cellar-by-richard-laymon.json").read_text())
    assert data["title"] == "The Cellar"
    assert data["kind"] == "Novel"


def test_creates_title_for_collection(
    mock_input: MockInput,
    author_fixture: repository_api.Author,
    title_fixture: repository_api.Title,
    tmp_path: Path,
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
            *enter_included_title_text(title_fixture.title),
            *select_title_search_result("y"),
            "n",
            "n",
        ]
    )

    add_title.prompt()

    slug = "the-richard-laymon-collection-volume-1-by-richard-laymon"
    data = json.loads((tmp_path / "titles" / f"{slug}.json").read_text())
    assert data["kind"] == "Collection"
    assert title_fixture.slug in data["includedTitles"]


def test_can_cancel_out_of_author_name(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input([Escape])

    add_title.prompt()

    assert len(list((tmp_path / "titles").glob("*.json"))) == 1


def test_can_cancel_out_of_kind(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input([Escape])

    add_title.prompt()

    assert len(list((tmp_path / "titles").glob("*.json"))) == 1
