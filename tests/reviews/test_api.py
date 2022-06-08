import os
from datetime import date

import pytest

from booklog.reviews import api as reviews_api
from booklog.reviews.review import TimelineEntry
from booklog.utils.sequence_tools import SequenceError


def test_create_serializes_new_review(tmp_path: str) -> None:
    expected = "---\nsequence: 1\nslug: on-writing-by-stephen-king\ngrade: A+\nedition: Kindle\nedition_notes:\ntimeline:\n- date: 2016-03-10\n  progress: 15%\n- date: 2016-03-11\n  progress: 50%\n- date: 2016-03-12\n  progress: Finished\n---\n\n"  # noqa: 501

    reviews_api.create(
        work_slug="on-writing-by-stephen-king",
        edition="Kindle",
        grade="A+",
        timeline=[
            TimelineEntry(date=date(2016, 3, 10), progress="15%"),
            TimelineEntry(date=date(2016, 3, 11), progress="50%"),
            TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
        ],
    )

    with open(
        os.path.join(tmp_path, "0001-on-writing-by-stephen-king.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == expected


def test_create_raises_error_if_sequence_out_of_sync(tmp_path: str) -> None:
    existing_review = "---\nsequence: 3\nslug: on-writing-by-stephen-king\ngrade: A+\nedition: Kindle\nedition_notes:\ntimeline:\n- date: 2016-03-10\n  progress: 15%\n- date: 2016-03-11\n  progress: 50%\n- date: 2016-03-12\n  progress: Finished\n---\n\n"  # noqa: 501

    with open(
        os.path.join(tmp_path, "0003-on-writing-by-stephen-king.md"),
        "w",
    ) as output_file:
        output_file.write(existing_review)

    with pytest.raises(SequenceError):
        reviews_api.create(
            work_slug="on-writing-by-stephen-king",
            edition="Kindle",
            grade="A+",
            timeline=[
                TimelineEntry(date=date(2016, 3, 10), progress="15%"),
                TimelineEntry(date=date(2016, 3, 11), progress="50%"),
                TimelineEntry(date=date(2016, 3, 12), progress="Finished"),
            ],
        )
