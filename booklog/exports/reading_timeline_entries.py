import datetime
from typing import Iterable, TypedDict

from booklog.exports import exporter
from booklog.repository.api import Reading, TimelineEntry
from booklog.utils.logging import logger

ExportsReadingTimelineEntryAuthor = TypedDict(
    "ExportsReadingTimelineEntryAuthor",
    {
        "name": str,
    },
)


ExportsReadingTimelineEntry = TypedDict(
    "ExportsReadingTimelineEntry",
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
        "authors": list[ExportsReadingTimelineEntryAuthor],
        "includedInSlugs": list[str],
    },
)


def build_json_reading_progress(
    reading: Reading,
    timeline_entry: TimelineEntry,
) -> ExportsReadingTimelineEntry:
    work = reading.work()
    reviewed = bool(work.review())

    return ExportsReadingTimelineEntry(
        sequence="{0}-{1}".format(timeline_entry.date, reading.sequence),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        yearPublished=work.year,
        title=work.title,
        readingYear=timeline_entry.date.year,
        authors=[
            ExportsReadingTimelineEntryAuthor(name=work_author.author().name)
            for work_author in work.work_authors
        ],
        includedInSlugs=[
            included_in_work.slug for included_in_work in work.included_in_works()
        ],
    )


def export(
    readings: Iterable[Reading],
) -> None:
    logger.log("==== Begin exporting {}...", "reading_timeline_entries")

    json_progress = [
        build_json_reading_progress(
            reading=reading,
            timeline_entry=timeline_entry,
        )
        for reading in readings
        for timeline_entry in reading.timeline
    ]

    exporter.serialize_dicts(
        sorted(json_progress, key=lambda progress: progress["sequence"], reverse=True),
        "reading-timeline-entries",
    )
