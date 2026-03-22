from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

import pytest
import yaml

from booklog.repository import api as repository_api
from booklog.repository.types import NonEmptyList

_FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def _read_yaml_frontmatter(file_path: Path) -> dict:  # type: ignore[type-arg]
    _, frontmatter, _ = _FM_REGEX.split(file_path.read_text(), 2)
    return yaml.safe_load(frontmatter)  # type: ignore[no-any-return]


@pytest.fixture
def author_fixture() -> repository_api.Author:
    return repository_api.create_author("Richard Laymon")


@pytest.fixture
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


def test_create_author(tmp_path: Path) -> None:
    repository_api.create_author(name="Stephen King")

    data = json.loads((tmp_path / "authors" / "stephen-king.json").read_text())

    assert data["name"] == "Stephen King"
    assert data["slug"] == "stephen-king"
    assert data["sortName"] == "King, Stephen"


def test_create_title(
    author_fixture: repository_api.Author,
    tmp_path: Path,
) -> None:
    repository_api.create_title(
        title="The Cellar",
        subtitle=None,
        year="1980",
        title_authors=NonEmptyList(
            repository_api.TitleAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ),
        kind="Novel",
    )

    data = json.loads((tmp_path / "titles" / "the-cellar-by-richard-laymon.json").read_text())

    assert data["title"] == "The Cellar"
    assert data["year"] == "1980"
    assert data["kind"] == "Novel"
    assert data["authors"][0]["slug"] == "richard-laymon"
    assert data["includedTitles"] == []


def test_create_title_with_included_titles(
    author_fixture: repository_api.Author,
    title_fixture: repository_api.Title,
    tmp_path: Path,
) -> None:
    repository_api.create_title(
        title="The Richard Laymon Collection Volume 1",
        subtitle=None,
        year="2006",
        title_authors=NonEmptyList(
            repository_api.TitleAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ),
        kind="Collection",
        included_title_ids=[title_fixture.slug],
    )

    slug = "the-richard-laymon-collection-volume-1-by-richard-laymon"
    data = json.loads((tmp_path / "titles" / f"{slug}.json").read_text())

    assert data["kind"] == "Collection"
    assert title_fixture.slug in data["includedTitles"]


def test_can_create_reading(
    tmp_path: Path,
    title_fixture: repository_api.Title,
) -> None:
    repository_api.create_reading(
        title=title_fixture,
        edition="Kindle",
        timeline=[
            repository_api.TimelineEntry(date=datetime.date(2016, 3, 10), progress="15%"),
            repository_api.TimelineEntry(date=datetime.date(2016, 3, 11), progress="50%"),
            repository_api.TimelineEntry(date=datetime.date(2016, 3, 12), progress="Finished"),
        ],
    )

    fm = _read_yaml_frontmatter(
        tmp_path / "readings" / "2016-03-12-01-the-cellar-by-richard-laymon.md"
    )

    assert fm["titleId"] == "the-cellar-by-richard-laymon"
    assert fm["edition"] == "Kindle"
    assert fm["date"] == datetime.date(2016, 3, 12)
    assert fm["timeline"][0]["progress"] == "15%"
    assert fm["timeline"][1]["progress"] == "50%"
    assert fm["timeline"][2]["progress"] == "Finished"


def test_can_create_new_review(
    tmp_path: Path,
    title_fixture: repository_api.Title,
) -> None:
    repository_api.create_or_update_review(
        title=title_fixture,
        grade="A+",
        date=datetime.date(2016, 3, 10),
    )

    fm = _read_yaml_frontmatter(tmp_path / "reviews" / "the-cellar-by-richard-laymon.md")

    assert fm["slug"] == "the-cellar-by-richard-laymon"
    assert fm["grade"] == "A+"
    assert fm["date"] == datetime.date(2016, 3, 10)


def test_can_update_existing_review(
    tmp_path: Path,
    title_fixture: repository_api.Title,
) -> None:
    existing_review = "---\nslug: the-cellar-by-richard-laymon\ngrade: A+\ndate: 2016-03-10\n---\n\nSome review content we want to preserve between updates."  # noqa: E501
    (tmp_path / "reviews" / "the-cellar-by-richard-laymon.md").write_text(existing_review)

    repository_api.create_or_update_review(
        title=title_fixture,
        grade="C+",
        date=datetime.date(2017, 3, 12),
    )

    review_path = tmp_path / "reviews" / "the-cellar-by-richard-laymon.md"
    fm = _read_yaml_frontmatter(review_path)

    assert fm["grade"] == "C+"
    assert fm["date"] == datetime.date(2017, 3, 12)
    assert "Some review content we want to preserve between updates." in review_path.read_text()


def test_title_author_with_invalid_slug_raises_error() -> None:
    """Test that TitleAuthor.author() raises ValueError for invalid slug."""
    title_author = repository_api.TitleAuthor(author_slug="non-existent-author", notes=None)

    with pytest.raises(ValueError, match="Author with slug 'non-existent-author' not found"):
        title_author.author()


def test_reading_with_invalid_title_id_raises_error() -> None:
    """Test that Reading.title() raises ValueError for invalid titleId."""
    reading = repository_api.Reading(
        sequence=1,
        edition="Kindle",
        timeline=[],
        slug="2024-01-01-01-non-existent-title",
        titleId="non-existent-title",
        date=datetime.date(2024, 1, 1),
    )

    with pytest.raises(ValueError, match="Title with slug 'non-existent-title' not found"):
        reading.title()


def test_review_with_invalid_title_slug_raises_error() -> None:
    """Test that Review.title() raises ValueError for invalid slug."""
    review = repository_api.Review(
        slug="non-existent-title", date=datetime.date(2024, 1, 1), grade="A+"
    )

    with pytest.raises(ValueError, match="Title with slug 'non-existent-title' not found"):
        review.title()
