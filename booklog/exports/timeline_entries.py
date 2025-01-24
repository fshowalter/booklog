import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger

JsonTimelineEntryAuthor = TypedDict(
    "JsonTimelineEntryAuthor",
    {
        "name": str,
    },
)


JsonTimelineEntry = TypedDict(
    "JsonTimelineEntry",
    {
        "sequence": str,
        "slug": str,
        "edition": str,
        "date": datetime.date,
        "progress": str,
        "reviewed": bool,
        "readingYear": str,
        "yearPublished": str,
        "title": str,
        "kind": str,
        "authors": list[JsonTimelineEntryAuthor],
        "includedInSlugs": list[str],
    },
)


def _build_json_timeline_entry(
    reading: repository_api.Reading,
    timeline_entry: repository_api.TimelineEntry,
    repository_data: RepositoryData,
) -> JsonTimelineEntry:
    work = reading.work(repository_data.works)
    reviewed = bool(work.review(repository_data.reviews))

    return JsonTimelineEntry(
        sequence="{0}-{1}-{2}".format(
            timeline_entry.date, reading.timeline[0].date, reading.sequence
        ),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        yearPublished=work.year,
        title=work.title,
        readingYear=str(timeline_entry.date.year),
        authors=[
            JsonTimelineEntryAuthor(
                name=work_author.author(repository_data.authors).name
            )
            for work_author in work.work_authors
        ],
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "timeline-entries")

    json_progress = [
        _build_json_timeline_entry(
            reading=reading,
            timeline_entry=timeline_entry,
            repository_data=repository_data,
        )
        for reading in repository_data.readings
        for timeline_entry in reading.timeline
    ]

    exporter.serialize_dicts(
        sorted(json_progress, key=lambda progress: progress["sequence"], reverse=True),
        "timeline-entries",
    )
