import datetime
from typing import Optional, TypedDict

from booklog.data.exports.utils import export_tools, list_tools
from booklog.data.readings.api import Reading
from booklog.data.reviews.api import Review
from booklog.logger import logger

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {"name": str, "sortName": str, "slug": str, "notes": Optional[str]},
)

JsonTimelineEntry = TypedDict(
    "JsonTimelineEntry",
    {"date": datetime.date, "progress": str},
)

JsonReading = TypedDict(
    "JsonReading",
    {
        "date": datetime.date,
        "edition": str,
        "editionNotes": Optional[str],
        "isAudioBook": bool,
        "readingTime": int,
        "abandoned": bool,
        "sequence": int,
        "timeline": list[JsonTimelineEntry],
    },
)


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
        "readings": list[JsonReading],
    },
)


def build_json_reading(reading: Reading) -> JsonReading:
    first_timeline_entry = sorted(reading.timeline, key=lambda entry: entry.date)[0]

    last_timeline_entry = sorted(
        reading.timeline, key=lambda entry: entry.date, reverse=True
    )[0]

    reading_time = (last_timeline_entry.date - first_timeline_entry.date).days + 1

    return JsonReading(
        sequence=reading.sequence,
        date=last_timeline_entry.date,
        edition=reading.edition,
        editionNotes=reading.edition_notes,
        isAudioBook=reading.edition == "Audible",
        abandoned=last_timeline_entry.progress == "Abandoned",
        readingTime=reading_time,
        timeline=[
            JsonTimelineEntry(
                date=timeline_entry.date, progress=timeline_entry.progress
            )
            for timeline_entry in reading.timeline
        ],
    )


def build_json_reviewed_work(
    readings: list[Reading],
    review: Review,
) -> JsonReviewedWork:
    most_recent_reading = sorted(
        readings, key=lambda reading: reading.sequence, reverse=True
    )[0]

    return JsonReviewedWork(
        sequence=most_recent_reading.sequence,
        slug=review.work.slug,
        title=review.work.title,
        sortTitle=review.work.sort_title,
        yearPublished=review.work.year,
        grade=review.grade,
        gradeValue=review.grade_value,
        kind=review.work.kind,
        date=review.date,
        authors=[
            JsonWorkAuthor(
                name=work_author.name,
                sortName=work_author.sort_name,
                slug=work_author.slug,
                notes=work_author.notes,
            )
            for work_author in review.work.authors
        ],
        readings=[build_json_reading(reading) for reading in readings],
        includedInSlugs=review.work.included_in_work_slugs,
        yearReviewed=review.date.year,
    )


def export(
    readings: list[Reading],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reviewed_works")

    json_reviewed_works = []

    readings_by_work_slug = list_tools.group_list_by_key(
        readings, lambda reading: reading.work.slug
    )

    for review in reviews:
        if not readings_by_work_slug[review.work.slug]:
            continue

        json_reviewed_works.append(
            build_json_reviewed_work(
                readings=readings_by_work_slug[review.work.slug],
                review=review,
            )
        )

    export_tools.serialize_dicts_to_folder(
        json_reviewed_works,
        "reviewed_works",
        filename_key=lambda work: work["slug"],
    )
