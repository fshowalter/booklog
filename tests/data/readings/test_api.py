import json
import os
from datetime import date
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.data.core import api as core_api
from booklog.data.readings import api as readings_api


@pytest.fixture
def created_author() -> core_api.Author:
    return core_api.create_author("Richard Laymon")


@pytest.fixture
def created_work(created_author: core_api.Author) -> core_api.Work:
    return core_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_work_slugs=[],
        work_authors=[
            core_api.WorkAuthor(
                name=created_author.name,
                sort_name=created_author.sort_name,
                slug=created_author.slug,
                notes=None,
            )
        ],
    )


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_can_create_reading(
    tmp_path: Path, created_work: core_api.Work, snapshot_json: SnapshotAssertion
) -> None:
    readings_api.create_reading(
        work=created_work,
        edition="Kindle",
        timeline=[
            readings_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            readings_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            readings_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )

    with open(
        os.path.join(tmp_path / "readings", "0001-the-cellar-by-richard-laymon.json"),
        "r",
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot_json


def test_create_raises_error_if_sequence_out_of_sync(
    tmp_path: Path, created_work: core_api.Work
) -> None:
    existing_reading = json.dumps(
        {
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
        },
        indent=4,
    )

    with open(
        os.path.join(tmp_path / "readings", "0003-on-writing-by-stephen-king.json"),
        "w",
    ) as output_file:
        output_file.write(existing_reading)

    with pytest.raises(readings_api.SequenceError):
        readings_api.create_reading(
            work=created_work,
            edition="Kindle",
            timeline=[
                readings_api.TimelineEntry(date=date(2016, 3, 10), progress="15%"),
                readings_api.TimelineEntry(date=date(2016, 3, 11), progress="50%"),
                readings_api.TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
            ],
        )
