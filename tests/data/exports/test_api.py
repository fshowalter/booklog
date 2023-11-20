import json
import os
from datetime import date
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.data.core import api as core_api
from booklog.data.exports import api as exports_api
from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api


@pytest.fixture(autouse=True)
def init_data() -> None:
    author = core_api.create_author("Stephen King")
    work = core_api.create_work(
        title="On Writing",
        subtitle="A Memoir of the Craft",
        year="2000",
        work_authors=[
            core_api.WorkAuthor(
                slug=author.slug,
                name=author.name,
                sort_name=author.sort_name,
                notes=None,
            )
        ],
        kind="Nonfiction",
    )
    readings_api.create_reading(
        work=work,
        edition="Kindle",
        timeline=[
            readings_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            readings_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            readings_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )
    reviews_api.create_or_update(
        work=work,
        grade="A+",
        date=date(2016, 3, 10),
    )


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_exports_reviewed_works(
    tmp_path: Path, snapshot_json: SnapshotAssertion
) -> None:
    exports_api.export_data()

    with open(
        os.path.join(
            tmp_path / "exports" / "reviewed_works", "on-writing-by-stephen-king.json"
        ),
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
