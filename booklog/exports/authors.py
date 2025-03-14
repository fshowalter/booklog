from typing import TypedDict

from booklog.exports import exporter, json_work_author
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonAuthorReviewedWork(TypedDict):
    title: str
    yearPublished: str
    kind: str
    slug: str
    sortTitle: str
    grade: str | None
    gradeValue: int | None
    authors: list[json_work_author.JsonWorkAuthor]
    includedInSlugs: list[str]


class JsonAuthor(TypedDict):
    name: str
    sortName: str
    slug: str
    reviewedWorks: list[JsonAuthorReviewedWork]


def _build_json_author_reviewed_work(
    work: repository_api.Work,
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonAuthorReviewedWork:
    return JsonAuthorReviewedWork(
        title=work.title,
        yearPublished=work.year,
        kind=work.kind,
        slug=work.slug,
        sortTitle=work.sort_title,
        grade=review.grade,
        gradeValue=review.grade_value,
        authors=[
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=repository_data.authors
            )
            for work_author in work.work_authors
        ],
        includedInSlugs=[work.slug for work in work.included_in_works(repository_data.works)],
    )


def _build_json_author(
    author: repository_api.Author, repository_data: RepositoryData
) -> JsonAuthor:
    author_works = list(author.works(repository_data.works))

    reviewed_works = []

    for work in author_works:
        review = work.review(repository_data.reviews)
        if review:
            reviewed_works.append(
                _build_json_author_reviewed_work(
                    work=work, review=review, repository_data=repository_data
                )
            )

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        reviewedWorks=reviewed_works,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "authors")

    json_authors = [
        _build_json_author(
            author=author,
            repository_data=repository_data,
        )
        for author in repository_data.authors
    ]

    exporter.serialize_dicts_to_folder(
        [json_author for json_author in json_authors if len(json_author["reviewedWorks"]) > 0],
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
