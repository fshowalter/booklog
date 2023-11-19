import json
import os
from datetime import date
from pathlib import Path

import pytest

from booklog.readings import api as readings_api
from booklog.readings.reading import TimelineEntry
from booklog.utils.sequence_tools import SequenceError


def test_create_serializes_new_reading(tmp_path: Path) -> None:
    expected = json.dumps(
        {
            "sequence": 1,
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

    readings_api.create(
        work_slug="on-writing-by-stephen-king",
        edition="Kindle",
        timeline=[
            TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )

    with open(
        os.path.join(tmp_path / "readings", "0001-on-writing-by-stephen-king.json"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == expected


def test_create_raises_error_if_sequence_out_of_sync(tmp_path: Path) -> None:
    existing_review = json.dumps(
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
        output_file.write(existing_review)

    with pytest.raises(SequenceError):
        readings_api.create(
            work_slug="on-writing-by-stephen-king",
            edition="Kindle",
            timeline=[
                TimelineEntry(date=date(2016, 3, 10), progress="15%"),
                TimelineEntry(date=date(2016, 3, 11), progress="50%"),
                TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
            ],
        )
