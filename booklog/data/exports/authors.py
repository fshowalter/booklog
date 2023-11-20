from typing import Optional, TypedDict

from booklog.data.core.api import AuthorWithWorks, Work
from booklog.data.exports.utils import export_tools, list_tools
from booklog.data.reviews.orm import Review
from booklog.logger import logger

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {"name": str, "sortName": str, "slug": str, "notes": Optional[str]},
)


JsonAuthorWork = TypedDict(
    "JsonAuthorWork",
    {
        "title": str,
        "yearPublished": str,
        "kind": str,
        "slug": str,
        "sortTitle": str,
        "grade": Optional[str],
        "gradeValue": Optional[int],
        "authors": list[JsonWorkAuthor],
        "reviewed": bool,
        "includedInSlugs": list[str],
    },
)

JsonAuthor = TypedDict(
    "JsonAuthor",
    {
        "name": str,
        "sortName": str,
        "slug": str,
        "reviewedWorkCount": int,
        "workCount": int,
        "works": list[JsonAuthorWork],
    },
)


def build_json_author_work(
    work: Work,
    review: Optional[Review],
) -> JsonAuthorWork:
    return JsonAuthorWork(
        title=work.title,
        yearPublished=work.year,
        kind=work.kind,
        slug=work.slug,
        sortTitle=work.sort_title,
        reviewed=bool(review),
        grade=review.grade if review else None,
        gradeValue=review.grade_value if review else None,
        authors=[
            JsonWorkAuthor(
                slug=work_author.slug,
                notes=work_author.notes,
                name=work_author.name,
                sortName=work_author.sort_name,
            )
            for work_author in work.authors
        ],
        includedInSlugs=work.included_in_work_slugs,
    )


def build_json_author(
    author: AuthorWithWorks,
    reviews_by_slug: dict[str, Review],
) -> JsonAuthor:
    reviewed_work_count = len(
        {author_work.slug for author_work in author.works} & reviews_by_slug.keys()
    )

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        works=[
            build_json_author_work(
                work=work,
                review=reviews_by_slug.get(work.slug),
            )
            for work in author.works
        ],
        reviewedWorkCount=reviewed_work_count,
        workCount=len(author.works),
    )


def export(
    authors: list[AuthorWithWorks],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "authors")

    reviews_by_slug = list_tools.list_to_dict_by_key(
        reviews, lambda review: review.work.slug
    )

    json_authors = [
        build_json_author(
            author=author,
            reviews_by_slug=reviews_by_slug,
        )
        for author in authors
    ]

    export_tools.serialize_dicts_to_folder(
        json_authors,
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
