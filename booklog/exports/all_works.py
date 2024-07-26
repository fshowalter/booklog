from typing import Optional, TypedDict

from booklog.exports import exporter, json_work_author
from booklog.exports.repository_data import RepositoryData
from booklog.utils.logging import logger

JsonWork = TypedDict(
    "JsonWork",
    {
        "slug": str,
        "includedInSlugs": list[str],
        "title": str,
        "subtitle": Optional[str],
        "authors": list[json_work_author.JsonWorkAuthor],
    },
)


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "unreviewed-works")

    json_works = [
        JsonWork(
            slug=work.slug,
            title=work.title,
            subtitle=work.subtitle,
            authors=[
                json_work_author.build_json_work_author(
                    work_author=work_author, all_authors=repository_data.authors
                )
                for work_author in work.work_authors
            ],
            includedInSlugs=[
                included_in_work.slug
                for included_in_work in work.included_in_works(repository_data.works)
            ],
        )
        for work in repository_data.works
        if not work.review(repository_data.reviews)
    ]

    exporter.serialize_dicts(
        json_works,
        "works",
    )
