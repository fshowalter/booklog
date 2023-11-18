from collections import defaultdict
from typing import Optional, TypedDict

from booklog.bookdata.api import Author, Work
from booklog.exports.json_work_author import JsonWorkAuthor, build_json_work_authors
from booklog.reviews.review import Review
from booklog.utils import export_tools, list_tools
from booklog.utils.logging import logger

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
    work: Work, works: list[Work], review: Optional[Review], authors: list[Author]
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
        authors=build_json_work_authors(work_authors=work.authors, authors=authors),
        includedInSlugs=[
            other_work.slug
            for other_work in works
            if work.slug in other_work.included_works
        ],
    )


def build_json_author(
    author: Author,
    authors: list[Author],
    author_works: list[Work],
    works: list[Work],
    reviews_by_slug: dict[str, Review],
) -> JsonAuthor:
    reviewed_work_count = len(
        {author_work.slug for author_work in author_works} & reviews_by_slug.keys()
    )

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        works=[
            build_json_author_work(
                work=work,
                works=works,
                review=reviews_by_slug.get(work.slug),
                authors=authors,
            )
            for work in author_works
        ],
        reviewedWorkCount=reviewed_work_count,
        workCount=len(author_works),
    )


def group_works_by_author(works: list[Work]) -> dict[str, list[Work]]:
    works_by_author = defaultdict(list)

    for work in works:
        for work_author in work.authors:
            works_by_author[work_author.slug].append(work)

    return works_by_author


def export(
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "authors")

    works_by_author = group_works_by_author(works)

    reviews_by_slug = list_tools.list_to_dict_by_key(
        reviews, lambda review: review.work_slug
    )

    for author in authors:
        json_authors = [
            build_json_author(
                author=author,
                authors=authors,
                author_works=works_by_author[author.slug],
                works=works,
                reviews_by_slug=reviews_by_slug,
            )
            for author in authors
        ]

    export_tools.serialize_dicts_to_folder(
        json_authors,
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
