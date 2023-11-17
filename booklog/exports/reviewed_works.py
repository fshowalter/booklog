import datetime
from typing import Optional, TypedDict

from booklog.bookdata.api import Author, Work
from booklog.exports.json_work_author import JsonWorkAuthor, build_json_work_authors
from booklog.readings.reading import Reading, TimelineEntry
from booklog.reviews.review import Review
from booklog.utils import export_tools, list_tools
from booklog.utils.logging import logger

JsonTimelineEntry = TypedDict("JsonTimelineEntry", {})


JsonReviewedWork = TypedDict(
    "JsonReviewedWork",
    {
        "sequence": int,
        "slug": str,
        "includedInSlugs": list[str],
        "title": str,
        "sortTitle": str,
        "yearPublished": str,
        "authors": list[JsonWorkAuthor],
        "grade": str,
        "gradeValue": int,
        "kind": str,
        "date": datetime.date,
        "yearReviewed": int,
    },
)


def build_json_reviewed_work(
    readings: list[Reading],
    authors: list[Author],
    work: Work,
    included_in_work_slugs: list[str],
    review: Review,
) -> JsonReviewedWork:
    most_recent_reading = sorted(
        readings, key=lambda reading: reading.sequence, reverse=True
    )[0]

    return JsonReviewedWork(
        sequence=most_recent_reading.sequence,
        slug=review.work_slug,
        title=work.title,
        sortTitle=work.sort_title,
        yearPublished=work.year,
        grade=review.grade,
        gradeValue=review.grade_value,
        kind=work.kind,
        date=review.date,
        authors=build_json_work_authors(work_authors=work.authors, authors=authors),
        includedInSlugs=included_in_work_slugs,
        yearReviewed=review.date.year,
    )


def export(
    readings: list[Reading],
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reviewed_works")

    json_reviewed_works = []

    works_by_slug = list_tools.list_to_dict_by_key(works, lambda work: work.slug)
    readings_by_work_slug = list_tools.group_list_by_key(
        readings, lambda reading: reading.work_slug
    )

    for review in reviews:
        if not readings_by_work_slug[review.work_slug]:
            continue

        json_reviewed_works.append(
            build_json_reviewed_work(
                readings=readings_by_work_slug[review.work_slug],
                authors=authors,
                work=works_by_slug[review.work_slug],
                review=review,
                included_in_work_slugs=[
                    work.slug
                    for work in works
                    if review.work_slug in work.included_works
                ],
            )
        )

    export_tools.serialize_dicts_to_folder(
        json_reviewed_works,
        "reviewed_works",
        filename_key=lambda work: work["slug"],
    )
