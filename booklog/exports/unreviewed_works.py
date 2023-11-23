from typing import Iterable, Optional, TypedDict

from booklog.exports import exporter, json_work_author
from booklog.repository.api import Work
from booklog.utils.logging import logger

ExportsUnreviewedWork = TypedDict(
    "ExportsUnreviewedWork",
    {
        "slug": str,
        "includedInSlugs": list[str],
        "title": str,
        "subtitle": Optional[str],
        "sortTitle": str,
        "yearPublished": str,
        "authors": list[json_work_author.JsonWorkAuthor],
        "kind": str,
    },
)


def export(
    works: Iterable[Work],
) -> None:
    logger.log("==== Begin exporting {}...", "unreviewed works")

    json_unreviewed_works = [
        ExportsUnreviewedWork(
            slug=work.slug,
            title=work.title,
            subtitle=work.subtitle,
            sortTitle=work.sort_title,
            yearPublished=work.year,
            kind=work.kind,
            authors=[
                json_work_author.build_json_work_author(work_author=work_author)
                for work_author in work.work_authors
            ],
            includedInSlugs=[
                included_in_work.slug for included_in_work in work.included_in_works()
            ],
        )
        for work in works
        if not work.review()
    ]

    exporter.serialize_dicts_to_folder(
        json_unreviewed_works,
        "unreviewed_works",
        filename_key=lambda work: work["slug"],
    )
