from typing import Optional, TypedDict

from booklog.exports import exporter, json_work_author
from booklog.repository import api as repository_api
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
        "authors": list[json_work_author.JsonWorkAuthor],
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
    work: repository_api.Work,
    review: Optional[repository_api.Review],
    all_works: list[repository_api.Work],
    all_authors: list[repository_api.Author],
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
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=all_authors
            )
            for work_author in work.work_authors
        ],
        includedInSlugs=[work.slug for work in work.included_in_works(all_works)],
    )


def build_json_author(
    author: repository_api.Author,
    all_works: list[repository_api.Work],
    all_reviews: list[repository_api.Review],
    all_authors: list[repository_api.Author],
) -> JsonAuthor:
    author_works = list(author.works(all_works))
    reviewed_work_count = len(
        [author_work for author_work in author_works if author_work.review(all_reviews)]
    )

    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        works=[
            build_json_author_work(
                work=work,
                review=work.review(all_reviews),
                all_works=all_works,
                all_authors=all_authors,
            )
            for work in author_works
        ],
        reviewedWorkCount=reviewed_work_count,
        workCount=len(author_works),
    )


def export(
    all_authors: list[repository_api.Author],
    all_works: list[repository_api.Work],
    all_reviews: list[repository_api.Review],
) -> None:
    logger.log("==== Begin exporting {}...", "authors")

    json_authors = [
        build_json_author(
            author=author,
            all_works=all_works,
            all_reviews=all_reviews,
            all_authors=all_authors,
        )
        for author in all_authors
    ]

    exporter.serialize_dicts_to_folder(
        json_authors,
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
