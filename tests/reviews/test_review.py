from datetime import date

import pytest

from booklog.reviews.review import ProgressMark, Review


@pytest.mark.parametrize(
    "grade, expected_grade_value",
    [
        ("A+", 5.33),
        ("A", 5.0),
        ("A-", 4.67),
        ("B+", 4.33),
        ("B", 4.0),
        ("B-", 3.67),
        ("C+", 3.33),
        ("C", 3.0),
        ("C-", 2.67),
        ("D+", 2.33),
        ("D", 2.0),
        ("D-", 1.67),
        ("F", 1.0),
    ],
)
def test_grade_value_accounts_for_modifers(
    grade: str, expected_grade_value: float
) -> None:
    review = Review(
        sequence=1,
        slug="on-writing-by-stephen-king",
        edition="Kindle",
        grade=grade,
        progress=[
            ProgressMark(date=date(2016, 3, 10), percent=15),
            ProgressMark(date=date(2016, 3, 11), percent=50),
            ProgressMark(date=date(2016, 3, 12), percent=100),
        ],
    )

    assert review.grade_value == expected_grade_value