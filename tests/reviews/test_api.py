import os
from datetime import date

import pytest

from booklog.reviews import api as reviews_api
from booklog.reviews.review import ProgressMark
from booklog.utils.sequence_tools import SequenceError


def test_create_serializes_new_review(tmp_path: str) -> None:
    expected = "---\nsequence: 1\nslug: on-writing-by-stephen-king\ngrade: A+\nedition: Kindle\nedition_notes:\nisbn:\nprogress:\n- date: 2016-03-10\n  percent: 15\n- date: 2016-03-11\n  percent: 50\n- date: 2016-03-12\n  percent: 100\n---\n\n"  # noqa: 501

    reviews_api.create(
        work_slug="on-writing-by-stephen-king",
        edition="Kindle",
        grade="A+",
        progress=[
            ProgressMark(date=date(2016, 3, 10), percent=15),
            ProgressMark(date=date(2016, 3, 11), percent=50),
            ProgressMark(date=date(2016, 3, 12), percent=100),
        ],
    )

    with open(
        os.path.join(tmp_path, "0001-on-writing-by-stephen-king.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == expected


def test_create_raises_error_if_sequence_out_of_sync(tmp_path: str) -> None:
    existing_review = "---\nsequence: 3\nslug: on-writing-by-stephen-king\ngrade: A+\nedition: Kindle\nedition_notes:\nisbn:\nprogress:\n- date: 2016-03-10\n  percent: 15\n- date: 2016-03-11\n  percent: 50\n- date: 2016-03-12\n  percent: 100\n---\n\n"  # noqa: 501

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
            progress=[
                ProgressMark(date=date(2016, 3, 10), percent=15),
                ProgressMark(date=date(2016, 3, 11), percent=50),
                ProgressMark(date=date(2016, 3, 12), percent=100),
            ],
        )
