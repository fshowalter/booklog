from dataclasses import dataclass, field

from booklog.repository import api as repository_api


@dataclass
class RepositoryData:
    authors: list[repository_api.Author]
    authors_with_reviews: set[str]
    works: list[repository_api.Work]
    readings: list[repository_api.Reading]
    reviews: list[repository_api.Review]
    work_year_sequence_map: dict[str, int] = field(default_factory=dict, init=False)
    author_sequence_map: dict[str, int] = field(default_factory=dict, init=False)
    title_sequence_map: dict[str, int] = field(default_factory=dict, init=False)
    review_sequence_map: dict[str, int] = field(default_factory=dict, init=False)
    grade_sequence_map: dict[str, int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """Calculate sequence maps after initialization."""
        self.work_year_sequence_map = self._build_work_year_sequence_map()
        self.author_sequence_map = self._build_author_sequence_map()
        self.title_sequence_map = self._build_title_sequence_map()
        self.review_sequence_map = self._build_review_sequence_map()
        self.grade_sequence_map = self._build_grade_sequence_map()

    def _build_work_year_sequence_map(self) -> dict[str, int]:
        """Build a mapping of work slugs to their numeric position based on year-author-title sort.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of "{work.year}-{first_author_sort_name}-{work.sort_title}".
        """

        def get_sort_key(work: repository_api.Work) -> str:
            first_author_sort_name = ""
            if work.work_authors:
                first_author = work.work_authors[0].author(self.authors)
                first_author_sort_name = first_author.sort_name
            return f"{work.year}-{first_author_sort_name}-{work.sort_title}"

        sorted_works = sorted(self.works, key=get_sort_key)
        return {work.slug: idx + 1 for idx, work in enumerate(sorted_works)}

    def _build_author_sequence_map(self) -> dict[str, int]:
        """Build a mapping of work slugs to their numeric position based on author-year-title sort.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of "{first_author_sort_name}-{work.year}-{work.sort_title}".
        """

        def get_sort_key(work: repository_api.Work) -> str:
            first_author_sort_name = ""
            if work.work_authors:
                first_author = work.work_authors[0].author(self.authors)
                first_author_sort_name = first_author.sort_name
            return f"{first_author_sort_name}-{work.year}-{work.sort_title}"

        sorted_works = sorted(self.works, key=get_sort_key)
        return {work.slug: idx + 1 for idx, work in enumerate(sorted_works)}

    def _build_title_sequence_map(self) -> dict[str, int]:
        """Build a mapping of work slugs to their numeric position based on title-author-year sort.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of "{work.sort_title}-{first_author_sort_name}-{work.year}".
        """

        def get_sort_key(work: repository_api.Work) -> str:
            first_author_sort_name = ""
            if work.work_authors:
                first_author = work.work_authors[0].author(self.authors)
                first_author_sort_name = first_author.sort_name
            return f"{work.sort_title}-{first_author_sort_name}-{work.year}"

        sorted_works = sorted(self.works, key=get_sort_key)
        return {work.slug: idx + 1 for idx, work in enumerate(sorted_works)}

    def _build_review_sequence_map(self) -> dict[str, int]:
        """Build a mapping of work slugs to their review sequence number.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of "{review.date}-{most_recent_reading.sequence}".
        """
        review_sequences: list[tuple[str, str]] = []  # (work_slug, sort_key)

        for review in self.reviews:
            work = review.work(self.works)
            readings = list(work.readings(self.readings))

            if readings:
                most_recent_reading = sorted(readings, key=lambda r: r.sequence, reverse=True)[0]
                sort_key = f"{review.date}-{most_recent_reading.sequence}"
                review_sequences.append((work.slug, sort_key))

        # Sort by the sort_key and create mapping
        sorted_sequences = sorted(review_sequences, key=lambda x: x[1])
        return {work_slug: idx + 1 for idx, (work_slug, _) in enumerate(sorted_sequences)}

    def _build_grade_sequence_map(self) -> dict[str, int]:
        """Build a mapping of work slugs to their grade sequence number.

        Returns a dictionary where keys are work slugs and values are their 1-based
        position in the sorted order of
        "{review.grade_value}-{review.date}-{most_recent_reading.sequence}".
        """
        grade_sequences: list[tuple[str, str]] = []  # (work_slug, sort_key)

        for review in self.reviews:
            work = review.work(self.works)
            readings = list(work.readings(self.readings))

            if readings:
                most_recent_reading = sorted(readings, key=lambda r: r.sequence, reverse=True)[0]
                sort_key = f"{review.grade_value:02d}-{review.date}-{most_recent_reading.sequence}"
                grade_sequences.append((work.slug, sort_key))

        # Sort by the sort_key and create mapping
        sorted_sequences = sorted(grade_sequences, key=lambda x: x[1])
        return {work_slug: idx + 1 for idx, (work_slug, _) in enumerate(sorted_sequences)}
