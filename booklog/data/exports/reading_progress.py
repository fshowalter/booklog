import datetime
from typing import TypedDict

from booklog.data.exports.utils import export_tools
from booklog.data.readings.api import Reading, TimelineEntry
from booklog.data.reviews.api import Review
from booklog.logger import logger

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


def build_json_reading_progress(
    reading: Reading,
    timeline_entry: TimelineEntry,
    reviewed: bool,
) -> JsonReadingProgress:
    return JsonReadingProgress(
        sequence="{0}-{1}".format(timeline_entry.date, reading.sequence),
        slug=reading.work.slug,
        edition=reading.edition,
        kind=reading.work.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        yearPublished=reading.work.year,
        title=reading.work.title,
        readingYear=timeline_entry.date.year,
        authors=[
            JsonReadingProgressAuthor(name=work_author.name)
            for work_author in reading.work.authors
        ],
        includedInSlugs=reading.work.included_in_work_slugs,
    )


def export(
    readings: list[Reading],
    reviews: list[Review],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_progress")

    reviewed_work_slugs = {review.work.slug for review in reviews}

    json_progress = [
        build_json_reading_progress(
            reading=reading,
            timeline_entry=timeline_entry,
            reviewed=reading.work.slug in reviewed_work_slugs,
        )
        for reading in readings
        for timeline_entry in reading.timeline
    ]

    export_tools.serialize_dicts(
        sorted(json_progress, key=lambda progress: progress["sequence"], reverse=True),
        "reading_progress",
    )
