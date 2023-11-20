from __future__ import annotations

from booklog.data.core import api as core_api
from booklog.data.exports import (
    authors,
    reading_progress,
    reading_stats,
    reviewed_works,
    unreviewed_works,
)
from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api


def export_data() -> None:
    (all_authors, all_works) = core_api.all_authors_and_works()

    all_readings = readings_api.all_readings(all_works=all_works)
    all_reviews = reviews_api.all_reviews(all_works=all_works)

    authors.export(authors=all_authors, reviews=all_reviews)
    unreviewed_works.export(works=all_works, reviews=all_reviews)
    reviewed_works.export(readings=all_readings, reviews=all_reviews)
    reading_progress.export(readings=all_readings, reviews=all_reviews)
    reading_stats.export(readings=all_readings, reviews=all_reviews)
