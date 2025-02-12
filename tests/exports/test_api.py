import json
from datetime import date
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.exports import api as exports_api
from booklog.repository import api as repository_api


@pytest.fixture(autouse=True)
def init_data() -> None:
    author = repository_api.create_author("Stephen King")

    work = repository_api.create_work(
        title="On Writing",
        subtitle="A Memoir of the Craft",
        year="2000",
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author.slug,
                notes=None,
            )
        ],
        kind="Nonfiction",
    )

    repository_api.create_work(
        title="The Stand",
        subtitle=None,
        year="1978",
        work_authors=[
            repository_api.WorkAuthor(
                author_slug=author.slug,
                notes=None,
            )
        ],
        kind="Novel",
    )

    repository_api.create_reading(
        work=work,
        edition="Kindle",
        timeline=[
            repository_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            repository_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            repository_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )
    repository_api.create_or_update_review(
        work=work,
        grade="A+",
        date=date(2016, 3, 10),
    )


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_exports_authors(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    exports_api.export_data()

    with Path.open(
        Path(tmp_path) / "exports" / "authors" / "stephen-king.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_exports_reviewed_works(
    tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    exports_api.export_data()

    with Path.open(
        Path(tmp_path) / "exports" / "reviewed-works.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_exports_unreviewed_works(
    tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    exports_api.export_data()

    with Path.open(
        Path(tmp_path) / "exports" / "unreviewed-works.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_exports_reading_timeline_entries(
    tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    exports_api.export_data()

    with Path.open(
        Path(tmp_path) / "exports" / "timeline-entries.json",
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
