from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonAuthor(TypedDict):
    name: str
    sortName: str
    slug: str


def _build_json_author(
    author: repository_api.Author,
    repository_data: RepositoryData,
) -> JsonAuthor | None:
    author_works = list(author.works(repository_data.works))
    reviewed_slugs = [
        work.slug for work in author_works if work.review(repository_data.reviews) is not None
    ]

    if len(reviewed_slugs) == 0:
        return None

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
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
        [json_author for json_author in json_authors if json_author is not None],
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
