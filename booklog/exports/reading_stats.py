from collections import defaultdict
from datetime import date
from typing import Callable, TypedDict, TypeVar

from booklog.exports import exporter, list_tools
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
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
    distribution_items: list[ListType], key: Callable[[ListType], str]
) -> list[JsonDistribution]:
    distribution = list_tools.group_list_by_key(distribution_items, key)

    return [
        JsonDistribution(name=key, count=len(distribution_values))
        for key, distribution_values in distribution.items()
    ]


def date_finished_or_abandoned(reading: repository_api.Reading) -> date:
    return next(
        timeline_entry.date
        for timeline_entry in reading.timeline
        if timeline_entry.progress in {"Finished", "Abandoned"}
    )


def group_readings_by_author(
    readings: list[repository_api.Reading], repository_data: RepositoryData
) -> dict[str, list[repository_api.Reading]]:
    readings_by_author: dict[str, list[repository_api.Reading]] = defaultdict(list)

    for reading in readings:
        for work_author in reading.work(repository_data.works).work_authors:
            readings_by_author[work_author.author_slug].append(reading)

    return readings_by_author


def build_json_most_read_author_reading(
    reading: repository_api.Reading, repository_data: RepositoryData
) -> JsonMostReadAuthorReading:
    work = reading.work(repository_data.works)

    return JsonMostReadAuthorReading(
        sequence=reading.sequence,
        date=date_finished_or_abandoned(reading=reading),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        title=work.title,
        yearPublished=work.year,
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
    )


def build_most_read_authors(
    readings: list[repository_api.Reading], repository_data: RepositoryData
) -> list[JsonMostReadAuthor]:
    readings_by_author = group_readings_by_author(
        readings=readings, repository_data=repository_data
    )

    return [
        JsonMostReadAuthor(
            name=next(
                author.name
                for author in repository_data.authors
                if author.slug == author_slug
            ),
            count=len(readings),
            slug=author_slug,
            readings=[
                build_json_most_read_author_reading(
                    reading=reading, repository_data=repository_data
                )
                for reading in readings
            ],
        )
        for author_slug, readings in readings_by_author.items()
        if len(readings) > 1
    ]


def build_grade_distribution(
    reviews: list[repository_api.Review],
) -> list[JsonDistribution]:
    return build_json_distributions(reviews, lambda review: review.grade)


def build_kind_distribution(works: list[repository_api.Work]) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: work.kind)


def build_edition_distribution(
    readings: list[repository_api.Reading],
) -> list[JsonDistribution]:
    return build_json_distributions(readings, lambda reading: reading.edition)


def build_decade_distribution(
    works: list[repository_api.Work],
) -> list[JsonDistribution]:
    return build_json_distributions(works, lambda work: "{0}0s".format(work.year[:3]))


def book_count(
    readings: list[repository_api.Reading], repository_data: RepositoryData
) -> int:
    works = [reading.work(repository_data.works) for reading in readings]

    return len([work for work in works if work.kind not in {"Short Story", "Novella"}])


def build_json_reading_stats(
    span: str,
    readings: list[repository_api.Reading],
    reviews: list[repository_api.Review],
    most_read_authors: list[JsonMostReadAuthor],
    repository_data: RepositoryData,
) -> JsonReadingStats:
    works = [reading.work(repository_data.works) for reading in readings]

    return JsonReadingStats(
        span=span,
        reviews=len(reviews),
        readWorks=len(readings),
        books=book_count(readings, repository_data=repository_data),
        gradeDistribution=build_grade_distribution(reviews),
        kindDistribution=build_kind_distribution(works),
        editionDistribution=build_edition_distribution(readings),
        decadeDistribution=build_decade_distribution(works),
        mostReadAuthors=most_read_authors,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    json_reading_stats = [
        build_json_reading_stats(
            span="all-time",
            reviews=repository_data.reviews,
            readings=repository_data.readings,
            most_read_authors=build_most_read_authors(
                readings=repository_data.readings, repository_data=repository_data
            ),
            repository_data=repository_data,
        )
    ]

    reviews_by_year = list_tools.group_list_by_key(
        repository_data.reviews, lambda review: str(review.date.year)
    )

    readings_by_year = list_tools.group_list_by_key(
        repository_data.readings,
        lambda reading: str(date_finished_or_abandoned(reading).year),
    )

    for year, readings_for_year in readings_by_year.items():
        json_reading_stats.append(
            build_json_reading_stats(
                span=year,
                reviews=reviews_by_year[year],
                readings=readings_for_year,
                most_read_authors=build_most_read_authors(
                    readings=readings_for_year, repository_data=repository_data
                ),
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        json_reading_stats,
        "reading_stats",
        filename_key=lambda stats: stats["span"],
    )
