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
    reading_sequence_map: dict[tuple[str, int], int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """Calculate sequence maps after initialization."""
        self.review_sequence_map = self._build_review_sequence_map()
        self.reading_sequence_map = self._build_reading_sequence_map()

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

    def _build_reading_sequence_map(self) -> dict[tuple[str, int], int]:
        """Build a mapping of reading (last_timeline_date, sequence) to their sort position.

        Returns a dictionary where keys are tuples of (last_timeline_date, sequence)
        and values are their 1-based position in the sorted order of
        "{last_timeline_date}-{sequence}".
        """
        reading_entries: list[tuple[tuple[str, int], str]] = []

        for reading in self.readings:
            if reading.timeline:
                last_timeline_date = str(reading.timeline[-1].date)
                # Key is a tuple for unique identification
                key = (last_timeline_date, reading.sequence)
                # Sort key for ordering
                sort_key = f"{last_timeline_date}-{reading.sequence}"
                reading_entries.append((key, sort_key))

        # Sort by the sort_key
        sorted_entries = sorted(reading_entries, key=lambda x: x[1])
        return {key: idx + 1 for idx, (key, _) in enumerate(sorted_entries)}
