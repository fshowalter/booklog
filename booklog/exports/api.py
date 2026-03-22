from __future__ import annotations

from booklog.exports import reading_log, reviewed_authors, reviewed_titles, stats
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def export_data() -> None:
    authors_with_reviews: set[str] = set()

    all_titles = list(repository_api.titles())
    reviews = list(repository_api.reviews())
    all_authors = list(repository_api.authors())

    for author in all_authors:
        if any(title.review(reviews) for title in author.titles(all_titles)):
            authors_with_reviews.add(author.slug)

    repository_data = RepositoryData(
        authors=sorted(all_authors, key=lambda author: author.sort_name),
        titles=sorted(all_titles, key=lambda title: title.sort_title),
        reviews=sorted(reviews, key=lambda review: review.slug),
        readings=sorted(repository_api.readings(), key=lambda reading: reading.sequence),
        authors_with_reviews=authors_with_reviews,
    )

    reviewed_authors.export(repository_data)
    reviewed_titles.export(repository_data)
    stats.export(repository_data)
    reading_log.export(repository_data)
