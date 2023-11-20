from collections import defaultdict
from datetime import date
from typing import Callable, Iterable, TypedDict, TypeVar

from booklog.data.core.api import Work
from booklog.data.exports.utils import export_tools, list_tools
from booklog.data.readings.api import Reading
from booklog.data.reviews.api import Review
from booklog.logger import logger

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
        "includedInSlugs": list[str],
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

ListType = TypeVar("ListType")


def build_json_distributions(
    distribution_items: Iterable[ListType], key: Callable[[ListType], str]
) -> list[JsonDistribution]:
    distribution = list_tools.group_list_by_key(distribution_items, key)

    return [
        JsonDistribution(name=key, count=len(distribution_values))
        for key, distribution_values in distribution.items()
    ]


def date_finished_or_abandoned(reading: Reading) -> date:
    return next(
        timeline_entry.date
        for timeline_entry in reading.timeline
        if timeline_entry.progress in {"Finished", "Abandoned"}
    )


def group_readings_by_author(
    readings: list[Reading],
) -> dict[str, list[Reading]]:
    readings_by_author: dict[str, list[Reading]] = defaultdict(list)

    for reading in readings:
        for work_author in reading.work.authors:
            readings_by_author[work_author.slug].append(reading)

    return readings_by_author


def build_most_read_authors(readings: list[Reading]) -> list[JsonMostReadAuthor]:
    readings_by_author = group_readings_by_author(readings=readings)

    return [
        JsonMostReadAuthor(
            name=next(
                reading_author.name
                for reading in readings
                for reading_author in reading.work.authors
                if reading_author.slug == author_slug
            ),
            count=len(readings),
            slug=author_slug,
            readings=[
                JsonMostReadAuthorReading(
                    sequence=reading.sequence,
                    date=date_finished_or_abandoned(reading=reading),
                    slug=reading.work.slug,
                    edition=reading.edition,
                    kind=reading.work.kind,
                    title=reading.work.title,
                    yearPublished=reading.work.year,
                    includedInSlugs=reading.work.included_in_work_slugs,
                )
                for reading in readings
            ],
        )
        for author_slug, readings in readings_by_author.items()
        if len(readings) > 1
    ]


def build_grade_distribution(reviews: list[Review]) -> list[JsonDistribution]:
    return build_json_distributions(reviews, lambda review: review.grade)


def build_kind_distribution(works: list[Work]) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: work.kind)


def build_edition_distribution(
    readings: list[Reading],
) -> list[JsonDistribution]:
    return build_json_distributions(readings, lambda reading: reading.edition)


def build_decade_distribution(works: list[Work]) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: "{0}0s".format(work.year[:3]))


def book_count(readings: list[Reading]) -> int:
    works = [reading.work for reading in readings]

    return len([work for work in works if work.kind not in {"Short Story", "Novella"}])


def build_json_reading_stats(
    span: str,
    readings: list[Reading],
    reviews: list[Review],
    most_read_authors: list[JsonMostReadAuthor],
) -> JsonReadingStats:
    works = [reading.work for reading in readings]

    return JsonReadingStats(
        span=span,
        reviews=len(reviews),
        readWorks=len(readings),
        books=book_count(readings),
        gradeDistribution=build_grade_distribution(reviews),
        kindDistribution=build_kind_distribution(works),
        editionDistribution=build_edition_distribution(readings),
        decadeDistribution=build_decade_distribution(works),
        mostReadAuthors=most_read_authors,
    )


def export(
    readings: list[Reading],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    json_reading_stats = [
        build_json_reading_stats(
            span="all-time",
            reviews=reviews,
            readings=readings,
            most_read_authors=build_most_read_authors(readings=readings),
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
            build_json_reading_stats(
                span=year,
                reviews=reviews_by_year[year],
                readings=readings_for_year,
                most_read_authors=build_most_read_authors(readings=readings),
            )
        )

    export_tools.serialize_dicts_to_folder(
        json_reading_stats,
        "reading_stats",
        filename_key=lambda stats: stats["span"],
    )
