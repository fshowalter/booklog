import datetime
import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.repository import api as repository_api


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


@pytest.fixture
def author_fixture() -> repository_api.Author:
    return repository_api.create_author("Richard Laymon")


@pytest.fixture
def work_fixture(author_fixture: repository_api.Author) -> repository_api.Work:
    return repository_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_work_slugs=[],
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ],
    )


def test_create_author(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    repository_api.create_author(name="Stephen King")

    with Path.open(
        Path(tmp_path) / "authors" / "stephen-king.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_create_create_work(
    author_fixture: repository_api.Author,
    tmp_path: Path,
    snapshot_json: SnapshotAssertion,
) -> None:
    repository_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author_fixture.slug,
                notes=None,
            )
        ],
        kind="Novel",
    )

    with Path.open(
        Path(tmp_path) / "works" / "the-cellar-by-richard-laymon.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_can_create_reading(
    tmp_path: Path, work_fixture: repository_api.Work, snapshot_json: SnapshotAssertion
) -> None:
    repository_api.create_reading(
        work=work_fixture,
        edition="Kindle",
        timeline=[
            repository_api.TimelineEntry(
                date=datetime.date(2016, 3, 10), progress="15%"
            ),
            repository_api.TimelineEntry(
                date=datetime.date(2016, 3, 11), progress="50%"
            ),
            repository_api.TimelineEntry(
                date=datetime.date(2016, 3, 12), progress="Finished"
            ),
        ],
    )

    with Path.open(
        Path(tmp_path) / "readings" / "2016-03-12-01-the-cellar-by-richard-laymon.md",
        "r",
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot_json


def test_can_create_new_review(
    tmp_path: Path, work_fixture: repository_api.Work, snapshot: SnapshotAssertion
) -> None:
    repository_api.create_or_update_review(
        work=work_fixture,
        grade="A+",
        date=datetime.date(2016, 3, 10),
    )

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md", "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


def test_can_update_existing_review(
    tmp_path: Path, work_fixture: repository_api.Work, snapshot: SnapshotAssertion
) -> None:
    existing_review = "---\nwork_slug: the-cellar-by-richard-laymon\ngrade: A+\ndate: 2016-03-10\n---\n\nSome review content we want to preserve between updates."  # noqa: E501

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md",
        "w",
    ) as first_output_file:
        first_output_file.write(existing_review)

    repository_api.create_or_update_review(
        work=work_fixture,
        grade="C+",
        date=datetime.date(2017, 3, 12),
    )

    with Path.open(
        Path(tmp_path) / "reviews" / "the-cellar-by-richard-laymon.md", "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


def test_work_author_with_invalid_slug_raises_error() -> None:
    """Test that WorkAuthor.author() raises ValueError for invalid slug."""
    work_author = repository_api.WorkAuthor(
        author_slug="non-existent-author",
        notes=None
    )

    with pytest.raises(ValueError, match="Author with slug 'non-existent-author' not found"):
        work_author.author()


def test_reading_with_invalid_work_slug_raises_error() -> None:
    """Test that Reading.work() raises ValueError for invalid slug."""
    reading = repository_api.Reading(
        sequence=1,
        edition="Kindle",
        timeline=[],
        work_slug="non-existent-work"
    )

    with pytest.raises(ValueError, match="Work with slug 'non-existent-work' not found"):
        reading.work()


def test_review_with_invalid_work_slug_raises_error() -> None:
    """Test that Review.work() raises ValueError for invalid slug."""
    review = repository_api.Review(
        work_slug="non-existent-work",
        date=datetime.date(2024, 1, 1),
        grade="A+"
    )

    with pytest.raises(ValueError, match="Work with slug 'non-existent-work' not found"):
        review.work()
