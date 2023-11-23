from __future__ import annotations

from booklog.exports import (
    authors,
    reading_stats,
    reading_timeline_entries,
    reviewed_works,
    unreviewed_works,
)
from booklog.repository import api as repository_api


def export_data() -> None:
    all_authors = list(repository_api.authors())
    all_works = list(repository_api.works())
    all_reviews = list(repository_api.reviews())
    all_readings = list(repository_api.readings())

    authors.export(
        all_authors=all_authors, all_works=all_works, all_reviews=all_reviews
    )
    reviewed_works.export(
        all_works=all_works,
        all_authors=all_authors,
        all_reviews=all_reviews,
        all_readings=all_readings,
    )
    reading_timeline_entries.export(readings=repository_api.readings())
    unreviewed_works.export(works=repository_api.works())
    reading_stats.export(
        readings=repository_api.readings(), reviews=repository_api.reviews()
    )
