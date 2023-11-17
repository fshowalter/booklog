from __future__ import annotations

from booklog.bookdata import api as bookdata_api
from booklog.exports import reading_progress, reviewed_works, unreviewed_works
from booklog.readings import api as readings_api
from booklog.reviews import api as reviews_api


def export_data() -> None:
    readings = readings_api.all_readings()
    works = bookdata_api.all_works()
    authors = bookdata_api.all_authors()
    reviews = reviews_api.all_reviews()

    reviewed_works.export(
        readings=readings, works=works, authors=authors, reviews=reviews
    )

    reading_progress.export(
        readings=readings, works=works, authors=authors, reviews=reviews
    )

    unreviewed_works.export(works=works, authors=authors, reviews=reviews)
