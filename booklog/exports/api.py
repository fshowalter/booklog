from __future__ import annotations

from booklog.exports import authors, more_for_reviewed_work, stats, works
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def export_data() -> None:
    authors_with_reviews: set[str] = set()

    all_works = list(repository_api.works())
    reviews = list(repository_api.reviews())
    all_authors = list(repository_api.authors())

    for author in all_authors:
        if any(work.review(reviews) for work in author.works(all_works)):
            authors_with_reviews.add(author.slug)

    repository_data = RepositoryData(
        authors=sorted(all_authors, key=lambda author: author.sort_name),
        works=sorted(all_works, key=lambda work: work.sort_title),
        reviews=sorted(reviews, key=lambda review: review.slug),
        readings=sorted(repository_api.readings(), key=lambda reading: reading.sequence),
        authors_with_reviews=authors_with_reviews,
    )

    authors.export(repository_data)
    more_for_reviewed_work.export(repository_data)
    stats.export(repository_data)
    works.export(repository_data)
