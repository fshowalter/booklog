import datetime
import json
import os
from pathlib import Path

import pytest
import yaml
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

    with open(
        os.path.join(tmp_path / "authors", "stephen-king.json"),
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

    with open(
        os.path.join(tmp_path / "works", "the-cellar-by-richard-laymon.json"),
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

    with open(
        os.path.join(tmp_path / "readings", "0001-the-cellar-by-richard-laymon.md"),
        "r",
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot_json


def test_create_raises_error_if_sequence_out_of_sync(
    tmp_path: Path, work_fixture: repository_api.Work
) -> None:
    existing_reading_data = {
        "sequence": 3,
        "work_slug": "on-writing-by-stephen-king",
        "edition": "Kindle",
        "timeline": [
            {
                "date": "2016-03-10",
                "progress": "15%",
            },
            {
                "date": "2016-03-11",
                "progress": "50%",
            },
            {
                "date": "2016-03-12",
                "progress": "Finished",
            },
        ],
        "edition_notes": None,
    }

    with open(
        os.path.join(tmp_path / "readings", "0003-on-writing-by-stephen-king.md"), "w"
    ) as markdown_file:
        markdown_file.write("---\n")
        yaml.dump(
            existing_reading_data,
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            stream=markdown_file,
        )
        markdown_file.write("---\n\n")

    with pytest.raises(repository_api.SequenceError):
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


def test_can_create_new_review(
    tmp_path: Path, work_fixture: repository_api.Work, snapshot: SnapshotAssertion
) -> None:
    repository_api.create_or_update_review(
        work=work_fixture,
        grade="A+",
        date=datetime.date(2016, 3, 10),
    )

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


def test_can_update_existing_review(
    tmp_path: Path, work_fixture: repository_api.Work, snapshot: SnapshotAssertion
) -> None:
    existing_review = "---\nwork_slug: the-cellar-by-richard-laymon\ngrade: A+\ndate: 2016-03-10\n---\n\nSome review content we want to preserve between updates."  # noqa: 501

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"),
        "w",
    ) as first_output_file:
        first_output_file.write(existing_review)

    repository_api.create_or_update_review(
        work=work_fixture,
        grade="C+",
        date=datetime.date(2017, 3, 12),
    )

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot
