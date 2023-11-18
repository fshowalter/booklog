from __future__ import annotations

from booklog.data.core import api as core_api
from booklog.data.exports import (  # reading_progress,; reading_stats,; reviewed_works,; unreviewed_works,
    authors,
)

# from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api


def export_data() -> None:
    all_json_authors = core_api.all_json_authors()
    all_json_works = core_api.all_json_works()

    # readings = readings_api.all_readings_with_work()
    # works = core_data_api.all_works()
    all_authors = core_api.all_authors(
        all_json_authors=all_json_authors, all_json_works=all_json_works
    )
    reviews = reviews_api.all_reviews()

    # reviewed_works.export(
    #     readings=readings, works=works, authors=all_authors, reviews=reviews
    # )

    # reading_progress.export(
    #     readings=readings, works=works, authors=all_authors, reviews=reviews
    # )

    # unreviewed_works.export(works=works, authors=all_authors, reviews=reviews)

    authors.export(authors=all_authors, reviews=reviews)

    # reading_stats.export(
    #     readings=readings, works=works, authors=all_authors, reviews=reviews
    # )
