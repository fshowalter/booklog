from __future__ import annotations

from typing import Optional

from booklog.reviews import editions, review, serializer
from booklog.utils import sequence_tools

TimelineEntry = review.TimelineEntry

Review = review.Review

all_editions = editions.all_editions

all_reviews = serializer.deserialize_all


def create(
    work_slug: str,
    timeline: list[TimelineEntry],
    edition: str,
    grade: Optional[str] = None,
) -> Review:
    sequence = sequence_tools.next_sequence(serializer.deserialize_all())

    new_review = review.Review(
        sequence=sequence,
        slug=work_slug,
        timeline=timeline,
        grade=grade,
        edition=edition,
    )

    serializer.serialize(new_review)

    return new_review
