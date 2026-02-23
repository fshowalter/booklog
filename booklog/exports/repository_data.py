from dataclasses import dataclass, field

from booklog.repository import api as repository_api


@dataclass
class RepositoryData:
    authors: list[repository_api.Author]
    authors_with_reviews: set[str]
    works: list[repository_api.Work]
    readings: list[repository_api.Reading]
    reviews: list[repository_api.Review]
    review_sequence_map: dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """Calculate sequence maps after initialization."""
        self.review_sequence_map = self._build_review_sequence_map()

    def _build_review_sequence_map(self) -> dict[str, str]:
        """Build a mapping of work slugs to their review sequence number.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of "{review.date}-{most_recent_reading.sequence}".
        """
        review_sequences: dict[str, str] = {}  # (work_slug, sort_key)

        for review in self.reviews:
            work = review.work(self.works)
            readings = list(work.readings(self.readings))

            if readings:
                most_recent_reading = sorted(readings, key=lambda r: r.sequence, reverse=True)[0]
                sort_key = f"{review.date}-{most_recent_reading.sequence:02}"
                review_sequences[work.slug] = sort_key

        return review_sequences

