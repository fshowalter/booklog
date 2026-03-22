import datetime
from collections import defaultdict
from collections.abc import Callable, Iterable
from datetime import date
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils import list_tools
from booklog.utils.logging import logger


class JsonMostReadAuthorWork(TypedDict):
    title: str
    readingDate: datetime.date
    edition: str
    reviewSlug: str | None


class JsonMostReadAuthor(TypedDict):
    count: int
    name: str
    authorSlug: str | None
    readTitles: list[JsonMostReadAuthorWork]


class JsonDistribution(TypedDict):
    name: str
    count: int


class JsonGradeDistribution(TypedDict):
    name: str
    count: int
    sortValue: int


class JsonYearStats(TypedDict):
    year: str
    titleCount: int
    bookCount: int
    kindDistribution: list[JsonDistribution]
    editionDistribution: list[JsonDistribution]
    decadeDistribution: list[JsonDistribution]
    mostReadAuthors: list[JsonMostReadAuthor]


class JsonAllTimeStats(TypedDict):
    reviewCount: int
    titleCount: int
    bookCount: int
    statsYears: list[str]
    gradeDistribution: list[JsonGradeDistribution]
    kindDistribution: list[JsonDistribution]
    editionDistribution: list[JsonDistribution]
    decadeDistribution: list[JsonDistribution]
    mostReadAuthors: list[JsonMostReadAuthor]


def _build_json_distributions[ListType](
    distribution_items: list[ListType], key: Callable[[ListType], str]
) -> list[JsonDistribution]:
    distribution = list_tools.group_list_by_key(distribution_items, key)

    json_distributions = [
        JsonDistribution(name=key, count=len(distribution_values))
        for key, distribution_values in distribution.items()
    ]

    return sorted(
        json_distributions,
        key=lambda json_distribution: json_distribution["name"],
    )


def _build_json_grade_distributions(
    reviews: Iterable[repository_api.Review],
) -> list[JsonGradeDistribution]:
    distribution = defaultdict(list)

    for review in reviews:
        distribution[(review.grade, review.grade_value or 0)].append(review)

    return sorted(
        [
            JsonGradeDistribution(name=grade, count=len(reviews), sortValue=grade_value)
            for (grade, grade_value), reviews in distribution.items()
        ],
        key=lambda distribution: distribution["sortValue"],
        reverse=True,
    )


def _date_finished_or_abandoned(reading: repository_api.Reading) -> date:
    return next(
        timeline_entry.date
        for timeline_entry in reading.timeline
        if timeline_entry.progress in {"Finished", "Abandoned"}
    )


def _group_readings_by_author(
    readings: list[repository_api.Reading], repository_data: RepositoryData
) -> dict[str, list[repository_api.Reading]]:
    readings_by_author: dict[str, list[repository_api.Reading]] = defaultdict(list)

    for reading in readings:
        title = reading.title(repository_data.titles)
        for title_author in title.title_authors:
            readings_by_author[title_author.author_slug].append(reading)

    return readings_by_author


def _build_most_read_author_titles(
    readings: list[repository_api.Reading], repository_data: RepositoryData
) -> list[JsonMostReadAuthorWork]:
    read_titles = []

    sorted_readings = sorted(readings, key=lambda reading: reading.slug)

    for reading in sorted_readings:
        title = reading.title(repository_data.titles)
        review = title.review(repository_data.reviews)

        read_titles.append(
            JsonMostReadAuthorWork(
                title=title.title,
                edition=reading.edition,
                readingDate=reading.date,
                reviewSlug=review.slug if review else None,
            )
        )

    return read_titles


def _build_most_read_authors(
    readings: list[repository_api.Reading],
    repository_data: RepositoryData,
) -> list[JsonMostReadAuthor]:
    readings_by_author = _group_readings_by_author(
        readings=readings, repository_data=repository_data
    )

    most_read_authors_list = [
        JsonMostReadAuthor(
            count=len(readings),
            name=next(
                author.name for author in repository_data.authors if author.slug == author_slug
            ),
            authorSlug=author_slug if author_slug in repository_data.authors_with_reviews else None,
            readTitles=_build_most_read_author_titles(readings, repository_data),
        )
        for author_slug, readings in readings_by_author.items()
        if len(readings) > 1
    ]

    return sorted(
        most_read_authors_list,
        key=lambda most_read_author: most_read_author["count"],
        reverse=True,
    )[:10]


def _build_kind_distribution(
    titles: list[repository_api.Title],
) -> list[JsonDistribution]:
    return _build_json_distributions(titles, lambda title: title.kind)


def _build_edition_distribution(
    readings: list[repository_api.Reading],
) -> list[JsonDistribution]:
    return _build_json_distributions(readings, lambda reading: reading.edition)


def _build_decade_distribution(
    titles: list[repository_api.Title],
) -> list[JsonDistribution]:
    return _build_json_distributions(titles, lambda title: f"{title.year[:3]}0s")


def _book_count(readings: list[repository_api.Reading], repository_data: RepositoryData) -> int:
    titles = [reading.title(repository_data.titles) for reading in readings]
    return len([title for title in titles if title.kind not in {"Short Story", "Novella"}])


def _build_year_json_stats(
    year: str,
    readings: list[repository_api.Reading],
    most_read_authors: list[JsonMostReadAuthor],
    repository_data: RepositoryData,
) -> JsonYearStats:
    titles = [reading.title(repository_data.titles) for reading in readings]

    return JsonYearStats(
        year=year,
        titleCount=len(readings),
        bookCount=_book_count(readings, repository_data=repository_data),
        kindDistribution=_build_kind_distribution(titles),
        editionDistribution=_build_edition_distribution(readings),
        decadeDistribution=_build_decade_distribution(titles),
        mostReadAuthors=most_read_authors,
    )


def _build_all_time_json_stats(
    readings: list[repository_api.Reading],
    reviews: list[repository_api.Review],
    most_read_authors: list[JsonMostReadAuthor],
    repository_data: RepositoryData,
    all_stats_years: list[str],
) -> JsonAllTimeStats:
    titles = [reading.title(repository_data.titles) for reading in readings]

    return JsonAllTimeStats(
        statsYears=all_stats_years,
        reviewCount=len(reviews),
        titleCount=len(readings),
        bookCount=_book_count(readings, repository_data=repository_data),
        gradeDistribution=_build_json_grade_distributions(reviews),
        kindDistribution=_build_kind_distribution(titles),
        editionDistribution=_build_edition_distribution(readings),
        decadeDistribution=_build_decade_distribution(titles),
        mostReadAuthors=most_read_authors,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    readings_by_year = list_tools.group_list_by_key(
        repository_data.readings,
        lambda reading: str(_date_finished_or_abandoned(reading).year),
    )

    all_stats_years = list(readings_by_year.keys())

    all_time_stats = _build_all_time_json_stats(
        reviews=repository_data.reviews,
        readings=repository_data.readings,
        most_read_authors=_build_most_read_authors(
            readings=repository_data.readings,
            repository_data=repository_data,
        ),
        repository_data=repository_data,
        all_stats_years=all_stats_years,
    )

    exporter.serialize_dict(
        all_time_stats,
        "all-time-stats",
    )

    year_stats = []

    for year, readings_for_year in readings_by_year.items():
        year_stats.append(
            _build_year_json_stats(
                year=year,
                readings=readings_for_year,
                most_read_authors=_build_most_read_authors(
                    readings=readings_for_year,
                    repository_data=repository_data,
                ),
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        year_stats,
        "year-stats",
        filename_key=lambda stats: stats["year"],
    )
