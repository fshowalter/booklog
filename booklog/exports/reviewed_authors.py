from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonAuthor(TypedDict):
    name: str
    sortName: str
    slug: str
    reviewedWorks: list[str]


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

        reviewed_works.append(work.slug)

    if not reviewed_works:
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
