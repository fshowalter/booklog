from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonWorkAuthor(TypedDict):
    name: str
    slug: str | None
    notes: str | None


def _build_json_work_author(
    work_author: repository_api.WorkAuthor, repository_data: RepositoryData
) -> JsonWorkAuthor:
    author = work_author.author(repository_data.authors)
    author_reviewed_works = [
        work for work in author.works(repository_data.works) if work.review(repository_data.reviews)
    ]

    return JsonWorkAuthor(
        name=author.name,
        slug=author.slug if len(author_reviewed_works) > 0 else None,
        notes=work_author.notes,
    )


class JsonWork(TypedDict):
    id: str
    title: str
    sortTitle: str
    subtitle: str | None
    year: str
    authors: list[JsonWorkAuthor]
    kind: str
    review: str | None


def _build_json_work(
    work: repository_api.Work,
    repository_data: RepositoryData,
) -> JsonWork:
    review = work.review(repository_data.reviews)

    return JsonWork(
        id=work.slug,
        title=work.title,
        subtitle=work.subtitle,
        sortTitle=work.sort_title,
        year=work.year,
        kind=work.kind,
        review=review.slug if review else None,
        authors=[
            _build_json_work_author(work_author, repository_data)
            for work_author in work.work_authors
        ],
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "works")

    json_works = []

    for work in repository_data.works:
        readings_for_work = list(work.readings(repository_data.readings))

        if len(readings_for_work) == 0:
            continue

        json_works.append(
            _build_json_work(
                work=work,
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        json_works,
        "works",
        filename_key=lambda json_work: json_work["id"],
    )
