from __future__ import annotations

import datetime

from booklog.reviews import review, serializer
from booklog.reviews.exports import api as exports_api

Review = review.Review

all_reviews = serializer.deserialize_all


def create(
    work_slug: str,
    date: datetime.date,
    grade: str = "Abandoned",
) -> Review:
    new_review = review.Review(
        work_slug=work_slug,
        date=date,
        grade=grade,
    )

    serializer.serialize(new_review)

    return new_review


def export_data() -> None:
    exports_api.export()
