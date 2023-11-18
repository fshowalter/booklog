from datetime import date
from typing import Any, TypedDict

from booklog.bookdata.api import Author, Work
from booklog.exports.json_work_author import JsonWorkAuthor, build_json_work_authors
from booklog.readings.reading import Reading
from booklog.reviews.review import Review
from booklog.utils import export_tools, list_tools
from booklog.utils.logging import logger

JsonTimelineEntry = TypedDict("JsonTimelineEntry", {})


JsonMostReadAuthorReading = TypedDict(
    "JsonMostReadAuthorReading",
    {
        "sequence": int,
        "date": date,
        "slug": str,
        "edition": str,
        "kind": str,
        "title": str,
        "yearPublished": str,
    },
)


JsonMostReadAuthor = TypedDict(
    "JsonMostReadAuthor",
    {
        "name": str,
        "count": int,
        "slug": str,
        "readings": list[JsonMostReadAuthorReading],
    },
)

JsonDistribution = TypedDict(
    "JsonDistribution",
    {
        "name": str,
        "count": int,
    },
)


JsonReadingStats = TypedDict(
    "JsonReadingStats",
    {
        "span": str,
        "reviews": int,
        "readWorks": int,
        "books": int,
        "gradeDistribution": list[JsonDistribution],
        "kindDistribution": list[JsonDistribution],
        "editionDistribution": list[JsonDistribution],
        "decadeDistribution": list[JsonDistribution],
        "mostReadAuthors": list[JsonMostReadAuthor],
    },
)


def build_json_distributions(
    distribution: dict[str, list[Any]]
) -> list[JsonDistribution]:
    return [
        JsonDistribution(name=key, count=len(distribution[key]))
        for key in distribution.keys()
    ]


def build_most_read_authors(readings: list[Reading], works: list[Work]) -> list[JsonMostReadAuthors]:
    readings_by_author: dict[str, list[Reading]] = defaultdict(list)

    for work in works:
        for author in work.authors
            works_by_author[author.slug].append


def extract_stats(
    span: str, reviews: list[Review], readings: list[Reading], works: list[Work]
) -> JsonReadingStats:
    return JsonReadingStats(
        span=span,
        reviews=len(reviews),
        readWorks=len(readings),
        books=len(
            [work for work in works if work.kind not in {"Short Story", "Novella"}]
        ),
        gradeDistribution=build_json_distributions(
            list_tools.group_list_by_key(reviews, lambda review: review.grade)
        ),
        kindDistribution=build_json_distributions(
            list_tools.group_list_by_key(works, lambda work: work.kind)
        ),
        editionDistribution=build_json_distributions(
            list_tools.group_list_by_key(readings, lambda reading: reading.edition)
        ),
        decadeDistribution=build_json_distributions(
            list_tools.group_list_by_key(
                works, lambda work: "{0}0s".format(work.year[:3])
            )
        ),
        mostReadAuthors=build_most_read_authors(readings=readings),
    )


def date_finished_or_abandoned(reading: Reading) -> date:
    return next(
        timeline_entry.date
        for timeline_entry in reading.timeline
        if timeline_entry.progress in {"Finished", "Abandoned"}
    )


def export(
    readings: list[Reading],
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    read_works = [
        work for reading in readings for work in works if work.slug == reading.work_slug
    ]

    json_reading_stats = [
        extract_stats(
            span="all-time",
            reviews=reviews,
            readings=readings,
            works=read_works,
        )
    ]

    reviews_by_year = list_tools.group_list_by_key(
        reviews, lambda review: str(review.date.year)
    )
    readings_by_year = list_tools.group_list_by_key(
        readings,
        lambda reading: str(date_finished_or_abandoned(reading).year),
    )

    for year, readings_for_year in readings_by_year.items():
        json_reading_stats.append(
            extract_stats(
                span=year,
                reviews=reviews_by_year[year],
                readings=readings_for_year,
                works=[
                    work
                    for work in works
                    if work.slug in {reading.work_slug for reading in readings_for_year}
                ],
            )
        )

    export_tools.serialize_dicts_to_folder(
        json_reading_stats,
        "reading_stats",
        filename_key=lambda stats: stats["span"],
    )
