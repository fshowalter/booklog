from __future__ import annotations

import datetime
from typing import Optional

from booklog.reviews import review, serializer

Review = review.Review

all_reviews = serializer.deserialize_all


def create(
    work_slug: str,
    date: datetime.date,
    grade: Optional[str] = None,
) -> Review:
    new_review = review.Review(
        work_slug=work_slug,
        date=date,
        grade=grade,
    )

    serializer.serialize(new_review)

    return new_review
