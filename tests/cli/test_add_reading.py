from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest
import yaml

from booklog.cli import add_reading
from booklog.repository import api as repository_api
from booklog.repository.types import NonEmptyList
from tests.cli.conftest import MockInput
from tests.cli.keys import Backspace, Escape
from tests.cli.prompt_utils import ConfirmType, enter_text, select_option

_FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def _read_yaml_frontmatter(file_path: Path) -> dict:  # type: ignore[type-arg]
    _, frontmatter, _ = _FM_REGEX.split(file_path.read_text(), 2)
    return yaml.safe_load(frontmatter)  # type: ignore[no-any-return]


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


@pytest.fixture(autouse=True)
def stub_editions(monkeypatch: pytest.MonkeyPatch) -> None:
    editions = ["Audible", "Hardback", "Kindle", "Paperback"]
    monkeypatch.setattr(repository_api, "reading_editions", lambda: editions)


def enter_title(title: str) -> list[str]:
    return enter_text(title)


def select_title_search_result(confirm: ConfirmType) -> list[str]:
    return select_option(1, confirm=confirm)


def select_search_again() -> list[str]:
    return select_option(1)


def select_edition_kindle() -> list[str]:
    return select_option(3)


def enter_date(date_str: str) -> list[str]:
    return [
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
        *enter_text(date_str),
    ]


def enter_progress(progress: str) -> list[str]:
    return enter_text(progress)


def enter_grade(grade: str) -> list[str]:
    return enter_text(grade)


def _assert_reading_created(tmp_path: Path) -> None:
    fm = _read_yaml_frontmatter(
        tmp_path / "readings" / "2016-03-12-01-the-cellar-by-richard-laymon.md"
    )
    assert fm["titleId"] == "the-cellar-by-richard-laymon"
    assert fm["edition"] == "Kindle"
    assert fm["timeline"][0]["progress"] == "15%"
    assert fm["timeline"][1]["progress"] == "50%"
    assert fm["timeline"][2]["progress"] == "Finished"


def _assert_review_created(tmp_path: Path) -> None:
    fm = _read_yaml_frontmatter(tmp_path / "reviews" / "the-cellar-by-richard-laymon.md")
    assert fm["grade"] == "A+"
    assert fm["date"] == date(2016, 3, 12)


def test_creates_reading_and_review(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
            "n",
        ]
    )

    add_reading.prompt()

    _assert_reading_created(tmp_path)
    _assert_review_created(tmp_path)


def test_can_search_again(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input(
        [
            *enter_title("The Typo"),
            *select_search_again(),
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
            "n",
        ]
    )

    add_reading.prompt()

    _assert_reading_created(tmp_path)
    _assert_review_created(tmp_path)


def test_can_escape_from_first_date(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            Escape,
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
            "n",
        ]
    )

    add_reading.prompt()

    _assert_reading_created(tmp_path)
    _assert_review_created(tmp_path)


def test_can_escape_from_second_progress_and_date(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            Escape,
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2017-03-11"),
            Escape,
            Escape,
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
            "n",
        ]
    )

    add_reading.prompt()

    _assert_reading_created(tmp_path)
    _assert_review_created(tmp_path)


def test_can_escape_from_progress(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input(
        [
            *enter_title("The Cellar"),
            *select_title_search_result(confirm="y"),
            *enter_date("2016-03-10"),
            *enter_progress("15"),
            *enter_date("2015-03-11"),
            Escape,
            *enter_date("2016-03-11"),
            *enter_progress("50"),
            *enter_date("2016-03-12"),
            *enter_progress("F"),
            *select_edition_kindle(),
            *enter_grade("A+"),
            "n",
        ]
    )

    add_reading.prompt()

    _assert_reading_created(tmp_path)
    _assert_review_created(tmp_path)


def test_can_escape_from_title(
    mock_input: MockInput,
    tmp_path: Path,
) -> None:
    mock_input([Escape])

    add_reading.prompt()

    assert list((tmp_path / "readings").glob("*.md")) == []
    assert list((tmp_path / "reviews").glob("*.md")) == []
