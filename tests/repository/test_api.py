import datetime
import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.repository import api as repository_api
from booklog.repository.types import NonEmptyList


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


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


def test_create_author(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    repository_api.create_author(name="Stephen King")

    with Path.open(
        Path(tmp_path) / "authors" / "stephen-king.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_create_title(
    author_fixture: repository_api.Author,
    tmp_path: Path,
    snapshot_json: SnapshotAssertion,
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

    with Path.open(
        Path(tmp_path) / "titles" / "the-cellar-by-richard-laymon.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_can_create_reading(
    tmp_path: Path, title_fixture: repository_api.Title, snapshot_json: SnapshotAssertion
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

    with Path.open(
        Path(tmp_path) / "readings" / "2016-03-12-01-the-cellar-by-richard-laymon.md",
        "r",
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot_json


def test_can_create_new_review(
    tmp_path: Path, title_fixture: repository_api.Title, snapshot: SnapshotAssertion
) -> None:
    repository_api.create_or_update_review(
        title=title_fixture,
        grade="A+",
        date=datetime.date(2016, 3, 10),
    )

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md", "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


def test_can_update_existing_review(
    tmp_path: Path, title_fixture: repository_api.Title, snapshot: SnapshotAssertion
) -> None:
    existing_review = "---\nslug: the-cellar-by-richard-laymon\ngrade: A+\ndate: 2016-03-10\n---\n\nSome review content we want to preserve between updates."  # noqa: E501

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md",
        "w",
    ) as first_output_file:
        first_output_file.write(existing_review)

    repository_api.create_or_update_review(
        title=title_fixture,
        grade="C+",
        date=datetime.date(2017, 3, 12),
    )

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md", "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


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
