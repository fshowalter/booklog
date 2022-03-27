from __future__ import annotations

from booklog.reviews import editions, review, serializer
from booklog.utils import sequence_tools

ProgressMark = review.ProgressMark

Review = review.Review

all_editions = editions.all_editions

all_reviews = serializer.deserialize_all


def create(
    work_slug: str, progress: list[ProgressMark], edition: str, grade: str
) -> Review:
    sequence = sequence_tools.next_sequence(serializer.deserialize_all())

    new_review = review.Review(
        sequence=sequence,
        slug=work_slug,
        progress=progress,
        grade=grade,
        edition=edition,
    )

    serializer.serialize(new_review)

    return new_review
