import os
from datetime import date

from booklog.reviews import api as reviews_api


def test_create_serializes_new_review(tmp_path: str) -> None:
    expected = "---\nwork_slug: on-writing-by-stephen-king\ngrade: A+\ndate: 2016-03-10\n---\n\n"  # noqa: 501

    reviews_api.create(
        work_slug="on-writing-by-stephen-king",
        grade="A+",
        date=date(2016, 3, 10),
    )

    with open(
        os.path.join(tmp_path, "on-writing-by-stephen-king.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == expected
