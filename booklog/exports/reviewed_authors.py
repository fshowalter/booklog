import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonWorkAuthor(TypedDict):
    notes: str | None
    name: str
    sortName: str
    slug: str


class JsonAuthorWork(TypedDict):
    id: str
    reviewSequence: str
    grade: str
    reviewDate: datetime.date
    title: str
    sortTitle: str
    workYear: str
    authors: list[JsonWorkAuthor]
    kind: str
    reviewSlug: str


class JsonAuthor(TypedDict):
    name: str
    sortName: str
    slug: str
    reviewedWorks: list[JsonAuthorWork]


def _build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)

    return JsonWorkAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        notes=work_author.notes,
    )


def _build_json_author_work(
    work: repository_api.Work,
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonAuthorWork:

    readings_for_work = list(work.readings(repository_data.readings))

    most_recent_reading = sorted(readings_for_work, key=lambda reading: reading.slug, reverse=True)[
        0
    ]

    return JsonAuthorWork(
        id=work.slug,
        reviewSequence=most_recent_reading.slug,
        reviewSlug=work.slug,
        title=work.title,
        sortTitle=work.sort_title,
        workYear=work.year,
        grade=review.grade,
        kind=work.kind,
        reviewDate=review.date,
        authors=[
            _build_json_work_author(work_author=work_author, all_authors=repository_data.authors)
            for work_author in work.work_authors
        ],
    )


def _build_json_author(
    author: repository_api.Author,
    repository_data: RepositoryData,
) -> JsonAuthor | None:
    author_works = list(author.works(repository_data.works))

    reviewed_works = []

    for work in author_works:
        review = work.review(repository_data.reviews)
        if review is None:
            continue

        reviewed_works.append(
            _build_json_author_work(work=work, review=review, repository_data=repository_data)
        )

    review_count = len(reviewed_works)

    if review_count == 0:
        return None

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        reviewedWorks=reviewed_works,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reviewed-authors")
    json_authors = []

    for author in repository_data.authors:
        json_author = _build_json_author(
            author=author,
            repository_data=repository_data,
        )

        if json_author is None:
            continue

        json_authors.append(json_author)

    exporter.serialize_dicts_to_folder(
        json_authors,
        "reviewed-authors",
        filename_key=lambda json_author: json_author["slug"],
    )
