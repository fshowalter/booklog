from typing import Optional, TypedDict

from booklog.data.core.api import Work
from booklog.data.exports.utils import export_tools
from booklog.data.reviews.api import Review
from booklog.logger import logger

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {"name": str, "sortName": str, "slug": str, "notes": Optional[str]},
)

JsonUnreviewedWork = TypedDict(
    "JsonUnreviewedWork",
    {
        "slug": str,
        "includedInSlugs": list[str],
        "title": str,
        "subtitle": Optional[str],
        "sortTitle": str,
        "yearPublished": str,
        "authors": list[JsonWorkAuthor],
        "kind": str,
    },
)


def export(
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "unreviewed works")

    reviewed_work_slugs = {review.work.slug for review in reviews}

    json_unreviewed_works = [
        JsonUnreviewedWork(
            slug=work.slug,
            title=work.title,
            subtitle=work.subtitle,
            sortTitle=work.sort_title,
            yearPublished=work.year,
            kind=work.kind,
            authors=[
                JsonWorkAuthor(
                    name=work_author.name,
                    sortName=work_author.sort_name,
                    slug=work_author.slug,
                    notes=work_author.notes,
                )
                for work_author in work.authors
            ],
            includedInSlugs=work.included_in_work_slugs,
        )
        for work in works
        if work.slug not in reviewed_work_slugs
    ]

    export_tools.serialize_dicts_to_folder(
        json_unreviewed_works,
        "unreviewed_works",
        filename_key=lambda work: work["slug"],
    )
