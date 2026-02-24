from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonWorkAuthor(TypedDict):
    slug: str
    notes: str | None


def _build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)

    return JsonWorkAuthor(
        slug=author.slug,
        notes=work_author.notes,
    )


class JsonWork(TypedDict):
    title: str
    subtitle: str | None
    sortTitle: str
    year: str
    authors: list[JsonWorkAuthor]
    kind: str
    slug: str
    includedWorks: list[str]


def _build_json_work(
    work: repository_api.Work,
    repository_data: RepositoryData,
) -> JsonWork:
    return JsonWork(
        title=work.title,
        subtitle=work.subtitle,
        sortTitle=work.sort_title,
        year=work.year,
        kind=work.kind,
        slug=work.slug,
        authors=[
            _build_json_work_author(work_author, repository_data.authors)
            for work_author in work.work_authors
        ],
        includedWorks=[
            included_work.slug for included_work in work.included_works(repository_data.works)
        ],
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "works")

    json_works = [
        _build_json_work(
            work=work,
            repository_data=repository_data,
        )
        for work in repository_data.works
    ]

    exporter.serialize_dicts_to_folder(
        json_works,
        "works",
        filename_key=lambda json_work: json_work["slug"],
    )
