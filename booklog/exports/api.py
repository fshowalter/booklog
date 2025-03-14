from __future__ import annotations

from collections import defaultdict

from booklog.exports import authors, reviewed_works, stats, timeline_entries
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def export_data() -> None:
    authors_with_reviews: dict[str, list[repository_api.Author]] =  defaultdict(list)

    works = list(repository_api.works())
    reviews = list(repository_api.reviews())
    all_authors = list(repository_api.authors())

    for author in all_authors:
        if any(work.review(reviews) for work in author.works(works)):
            authors_with_reviews[author.slug].append(author)


    repository_data = RepositoryData(
        authors=sorted(all_authors, key=lambda author: author.sort_name),
        works=sorted(works, key=lambda work: work.sort_title),
        reviews=sorted(reviews, key=lambda review: review.work_slug),
        readings=sorted(repository_api.readings(), key=lambda reading: reading.sequence),
        authors_with_reviews= authors_with_reviews
    )

    authors.export(repository_data)
    reviewed_works.export(repository_data)
    timeline_entries.export(repository_data)
    stats.export(repository_data)
