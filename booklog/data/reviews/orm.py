from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional, cast

from booklog.data.core import api as core_api
from booklog.data.reviews import markdown_reviews


@dataclass
class Review(object):
    work: core_api.Work
    date: datetime.date
    grade: str
    review_content: Optional[str] = None

    @property
    def grade_value(self) -> int:
        if self.grade == "Abandoned":
            return 0

        value_modifier = 1

        grade_map = {
            "A": 12,
            "B": 9,
            "C": 6,
            "D": 3,
        }

        grade_value = grade_map.get(self.grade[0], 1)
        modifier = self.grade[-1]

        if modifier == "+":
            grade_value += value_modifier

        if modifier == "-":
            grade_value -= value_modifier

        return grade_value


def create_or_update(
    work: core_api.Work,
    date: datetime.date,
    grade: str = "Abandoned",
) -> Review:
    return hydrate_markdown_review(
        markdown_review=markdown_reviews.create_or_update(
            work_slug=work.slug,
            date=datetime.date.isoformat(date),
            grade=grade,
        ),
        work=work,
    )


def hydrate_markdown_review(
    markdown_review: markdown_reviews.MarkdownReview,
    work: core_api.Work,
) -> Review:
    return Review(
        work=work,
        date=cast(datetime.date, markdown_review.yaml["date"]),
        grade=markdown_review.yaml["grade"],
        review_content=markdown_review.review_content,
    )
