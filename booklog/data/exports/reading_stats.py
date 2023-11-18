from collections import defaultdict
from datetime import date
from typing import Callable, Iterable, TypedDict, TypeVar

from booklog.bookdata.api import Author, Work
from booklog.readings.api import ReadingWithWork
from booklog.reviews.review import Review
from booklog.utils import export_tools, list_tools
from booklog.utils.logging import logger

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


def date_finished_or_abandoned(reading: ReadingWithWork) -> date:
    return next(
        timeline_entry.date
        for timeline_entry in reading.timeline
        if timeline_entry.progress in {"Finished", "Abandoned"}
    )


def group_readings_by_author(
    readings: list[ReadingWithWork], works: list[Work]
) -> dict[str, list[JsonMostReadAuthorReading]]:
    readings_by_author: dict[str, list[JsonMostReadAuthorReading]] = defaultdict(list)

    for reading in readings:
        for work_author in reading.work.authors:
            readings_by_author[work_author.slug].append(
                JsonMostReadAuthorReading(
                    sequence=reading.sequence,
                    date=date_finished_or_abandoned(reading=reading),
                    slug=reading.work.slug,
                    edition=reading.edition,
                    kind=reading.work.kind,
                    title=reading.work.title,
                    yearPublished=reading.work.year,
                    includedInSlugs=[
                        work.slug
                        for work in works
                        if reading.work_slug in work.included_works
                    ],
                )
            )

    return readings_by_author


def build_most_read_authors(
    readings: list[ReadingWithWork], works: list[Work], authors: list[Author]
) -> list[JsonMostReadAuthor]:
    readings_by_author = group_readings_by_author(readings=readings, works=works)

    return [
        JsonMostReadAuthor(
            name=next(author.name for author in authors if author.slug == author_slug),
            count=len(json_readings),
            slug=author_slug,
            readings=json_readings,
        )
        for author_slug, json_readings in readings_by_author.items()
        if len(json_readings) > 1
    ]


def build_grade_distribution(reviews: list[Review]) -> list[JsonDistribution]:
    return build_json_distributions(reviews, lambda review: review.grade)


def build_kind_distribution(works: list[Work]) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: work.kind)


def build_edition_distribution(
    readings: list[ReadingWithWork],
) -> list[JsonDistribution]:
    return build_json_distributions(readings, lambda reading: reading.edition)


def build_decade_distribution(works: list[Work]) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: "{0}0s".format(work.year[:3]))


def book_count(readings: list[ReadingWithWork]) -> int:
    works = [reading.work for reading in readings]

    return len([work for work in works if work.kind not in {"Short Story", "Novella"}])


def build_json_reading_stats(
    span: str,
    readings: list[ReadingWithWork],
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
    readings: list[ReadingWithWork],
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    json_reading_stats = [
        build_json_reading_stats(
            span="all-time",
            reviews=reviews,
            readings=readings,
            most_read_authors=build_most_read_authors(
                readings=readings, works=works, authors=authors
            ),
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
                most_read_authors=build_most_read_authors(
                    readings=readings, works=works, authors=authors
                ),
            )
        )

    export_tools.serialize_dicts_to_folder(
        json_reading_stats,
        "reading_stats",
        filename_key=lambda stats: stats["span"],
    )
