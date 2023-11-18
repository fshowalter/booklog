from typing import TypedDict

from booklog.bookdata.api import Author, Work
from booklog.exports.json_work_author import JsonWorkAuthor, build_json_work_authors
from booklog.reviews.review import Review
from booklog.utils import export_tools
from booklog.utils.logging import logger

JsonUnreviewedWork = TypedDict(
    "JsonUnreviewedWork",
    {
        "slug": str,
        "includedInSlugs": list[str],
        "title": str,
        "sortTitle": str,
        "yearPublished": str,
        "authors": list[JsonWorkAuthor],
        "kind": str,
    },
)


def export(
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "unreviewed works")

    reviewed_work_slugs = {review.work_slug for review in reviews}

    json_unreviewed_works = [
        JsonUnreviewedWork(
            slug=work.slug,
            title=work.title,
            sortTitle=work.sort_title,
            yearPublished=work.year,
            kind=work.kind,
            authors=build_json_work_authors(work_authors=work.authors, authors=authors),
            includedInSlugs=[
                other_work.slug
                for other_work in works
                if work.slug in other_work.included_works
            ],
        )
        for work in works
        if work.slug not in reviewed_work_slugs
    ]

    export_tools.serialize_dicts_to_folder(
        json_unreviewed_works,
        "unreviewed_works",
        filename_key=lambda work: work["slug"],
    )
