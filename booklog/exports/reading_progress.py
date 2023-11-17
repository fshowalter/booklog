import datetime
from typing import TypedDict

from booklog.bookdata.api import Author, Work, WorkAuthor
from booklog.readings.reading import Reading, TimelineEntry
from booklog.reviews.review import Review
from booklog.utils import export_tools, list_tools
from booklog.utils.logging import logger

JsonReadingProgressAuthor = TypedDict(
    "JsonReadingProgressAuthor",
    {
        "name": str,
    },
)


JsonReadingProgress = TypedDict(
    "JsonReadingProgress",
    {
        "sequence": str,
        "slug": str,
        "edition": str,
        "date": datetime.date,
        "progress": str,
        "reviewed": bool,
        "readingYear": int,
        "yearPublished": str,
        "title": str,
        "kind": str,
        "authors": list[JsonReadingProgressAuthor],
        "includedInSlugs": list[str],
    },
)


def build_json_reading_progress_authors(
    work_authors: list[WorkAuthor], authors: list[Author]
) -> list[JsonReadingProgressAuthor]:
    json_reading_progress_authors = []

    for work_author in work_authors:
        author = next(author for author in authors if author.slug in work_author.slug)

        json_reading_progress_authors.append(
            JsonReadingProgressAuthor(
                name=author.name,
            )
        )

    return json_reading_progress_authors


def build_json_reading_progress(
    reading: Reading,
    timeline_entry: TimelineEntry,
    authors: list[Author],
    work: Work,
    reviewed: bool,
    included_in_work_slugs: list[str],
) -> JsonReadingProgress:
    return JsonReadingProgress(
        sequence="{0}-{1}".format(timeline_entry.date, reading.sequence),
        slug=reading.work_slug,
        edition=reading.edition,
        kind=work.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        yearPublished=work.year,
        title=work.title,
        readingYear=timeline_entry.date.year,
        authors=build_json_reading_progress_authors(
            work_authors=work.authors, authors=authors
        ),
        includedInSlugs=included_in_work_slugs,
    )


def export(
    readings: list[Reading],
    authors: list[Author],
    works: list[Work],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_progress")

    works_by_slug = list_tools.list_to_dict_by_key(works, lambda work: work.slug)
    reviewed_work_slugs = {review.work_slug for review in reviews}

    json_progress = [
        build_json_reading_progress(
            reading=reading,
            timeline_entry=timeline_entry,
            authors=authors,
            work=works_by_slug[reading.work_slug],
            reviewed=reading.work_slug in reviewed_work_slugs,
            included_in_work_slugs=[
                work.slug for work in works if reading.work_slug in work.included_works
            ],
        )
        for reading in readings
        for timeline_entry in reading.timeline
    ]

    export_tools.serialize_dicts(
        sorted(json_progress, key=lambda progress: progress["sequence"], reverse=True),
        "reading_progress",
    )
