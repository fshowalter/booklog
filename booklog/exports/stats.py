from collections import defaultdict
from collections.abc import Callable, Iterable
from datetime import date
from typing import TypedDict, TypeVar

from booklog.exports import exporter, list_tools
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonMostReadAuthorReading(TypedDict):
    readingSequence: int
    date: date
    slug: str
    edition: str
    kind: str
    title: str
    workYear: str
    workYearSequence: int
    authorSequence: int
    titleSequence: int
    includedInSlugs: list[str]
    reviewed: bool


class JsonMostReadAuthor(TypedDict):
    name: str
    count: int
    slug: str
    reviewed: bool
    readings: list[JsonMostReadAuthorReading]


class JsonDistribution(TypedDict):
    name: str
    count: int


class JsonGradeDistribution(TypedDict):
    name: str
    count: int
    sortValue: int


class JsonYearStats(TypedDict):
    year: str
    workCount: int
    bookCount: int
    kindDistribution: list[JsonDistribution]
    editionDistribution: list[JsonDistribution]
    decadeDistribution: list[JsonDistribution]
    mostReadAuthors: list[JsonMostReadAuthor]


class JsonAllTimeStats(TypedDict):
    reviewCount: int
    workCount: int
    bookCount: int
    gradeDistribution: list[JsonGradeDistribution]
    kindDistribution: list[JsonDistribution]
    editionDistribution: list[JsonDistribution]
    decadeDistribution: list[JsonDistribution]
    mostReadAuthors: list[JsonMostReadAuthor]


ListType = TypeVar("ListType")


def _build_json_distributions(
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
        work = reading.work(repository_data.works)
        for work_author in work.work_authors:
            readings_by_author[work_author.author_slug].append(reading)

    return readings_by_author


def _build_json_most_read_author_reading(
    reading: repository_api.Reading,
    repository_data: RepositoryData,
) -> JsonMostReadAuthorReading:
    work = reading.work(repository_data.works)
    reviewed = bool(work.review(repository_data.reviews))

    # Get last timeline date for the reading sequence lookup
    last_timeline_date = _date_finished_or_abandoned(reading=reading)
    reading_key = (str(last_timeline_date), reading.sequence)
    reading_sequence = repository_data.reading_sequence_map.get(reading_key, 0)

    return JsonMostReadAuthorReading(
        readingSequence=reading_sequence,
        date=last_timeline_date,
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        title=work.title,
        workYear=work.year,
        workYearSequence=repository_data.work_year_sequence_map.get(work.slug, 0),
        authorSequence=repository_data.author_sequence_map.get(work.slug, 0),
        titleSequence=repository_data.title_sequence_map.get(work.slug, 0),
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
        reviewed=reviewed,
    )


def _reading_sort_key(reading: JsonMostReadAuthorReading) -> str:
    return "{}-{}".format(reading["date"], reading["readingSequence"])


def _build_most_read_authors(
    readings: list[repository_api.Reading],
    repository_data: RepositoryData,
) -> list[JsonMostReadAuthor]:
    readings_by_author = _group_readings_by_author(
        readings=readings, repository_data=repository_data
    )

    most_read_authors_list = [
        JsonMostReadAuthor(
            name=next(
                author.name for author in repository_data.authors if author.slug == author_slug
            ),
            count=len(readings),
            slug=author_slug,
            reviewed=author_slug in repository_data.authors_with_reviews,
            readings=sorted(
                [
                    _build_json_most_read_author_reading(
                        reading=reading,
                        repository_data=repository_data,
                    )
                    for reading in readings
                ],
                key=_reading_sort_key,
            ),
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
    works: list[repository_api.Work],
) -> list[JsonDistribution]:
    return _build_json_distributions(works, lambda work: work.kind)


def _build_edition_distribution(
    readings: list[repository_api.Reading],
) -> list[JsonDistribution]:
    return _build_json_distributions(readings, lambda reading: reading.edition)


def _build_decade_distribution(
    works: list[repository_api.Work],
) -> list[JsonDistribution]:
    return _build_json_distributions(works, lambda work: f"{work.year[:3]}0s")


def _book_count(readings: list[repository_api.Reading], repository_data: RepositoryData) -> int:
    works = [reading.work(repository_data.works) for reading in readings]
    return len([work for work in works if work.kind not in {"Short Story", "Novella"}])


def _build_year_json_stats(
    year: str,
    readings: list[repository_api.Reading],
    most_read_authors: list[JsonMostReadAuthor],
    repository_data: RepositoryData,
) -> JsonYearStats:
    works = [reading.work(repository_data.works) for reading in readings]

    return JsonYearStats(
        year=year,
        workCount=len(readings),
        bookCount=_book_count(readings, repository_data=repository_data),
        kindDistribution=_build_kind_distribution(works),
        editionDistribution=_build_edition_distribution(readings),
        decadeDistribution=_build_decade_distribution(works),
        mostReadAuthors=most_read_authors,
    )


def _build_all_time_json_stats(
    readings: list[repository_api.Reading],
    reviews: list[repository_api.Review],
    most_read_authors: list[JsonMostReadAuthor],
    repository_data: RepositoryData,
) -> JsonAllTimeStats:
    works = [reading.work(repository_data.works) for reading in readings]

    return JsonAllTimeStats(
        reviewCount=len(reviews),
        workCount=len(readings),
        bookCount=_book_count(readings, repository_data=repository_data),
        gradeDistribution=_build_json_grade_distributions(reviews),
        kindDistribution=_build_kind_distribution(works),
        editionDistribution=_build_edition_distribution(readings),
        decadeDistribution=_build_decade_distribution(works),
        mostReadAuthors=most_read_authors,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reading_stats")

    all_time_stats = _build_all_time_json_stats(
        reviews=repository_data.reviews,
        readings=repository_data.readings,
        most_read_authors=_build_most_read_authors(
            readings=repository_data.readings,
            repository_data=repository_data,
        ),
        repository_data=repository_data,
    )

    exporter.serialize_dict(
        all_time_stats,
        "all-time-stats",
    )

    year_stats = []

    readings_by_year = list_tools.group_list_by_key(
        repository_data.readings,
        lambda reading: str(_date_finished_or_abandoned(reading).year),
    )

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
