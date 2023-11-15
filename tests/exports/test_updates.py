import json
import os
from datetime import date
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.bookdata import api as bookdata_api
from booklog.exports import api
from booklog.readings import api as readings_api
from booklog.reviews import api as reviews_api


@pytest.fixture(autouse=True)
def init_data() -> None:
    author = bookdata_api.create_author("Stephen King")
    work = bookdata_api.create_work(
        title="On Writing",
        subtitle="A Memoir of the Craft",
        year="2000",
        authors=[bookdata_api.WorkAuthor(slug=author.slug, notes=None)],
        kind="Nonfiction",
    )
    readings_api.create(
        work_slug=work.slug,
        edition="Kindle",
        timeline=[
            readings_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            readings_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            readings_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )
    reviews_api.create(
        work_slug=work.slug,
        grade="A+",
        date=date(2016, 3, 10),
    )


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_exports_updates(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    api.export_data()

    with open(os.path.join(tmp_path / "exports", "updates.json"), "r") as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
