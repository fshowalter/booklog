import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.list_tools import group_list_by_key
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonWorkAuthor(TypedDict):
    notes: str | None
    name: str


class JsonReadingLogEntry(TypedDict):
    sequence: str
    reviewSlug: str | None
    id: str
    edition: str
    date: datetime.date
    progress: str
    workYear: str
    title: str
    kind: str
    authors: list[JsonWorkAuthor]


def _build_json_reading_entry_author(
    work_author: repository_api.WorkAuthor, authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(authors)
    return JsonWorkAuthor(name=author.name, notes=work_author.notes)


def _build_json_reading_log_entry(
    reading: repository_api.Reading,
    timeline_entry: repository_api.TimelineEntry,
    timeline_index: int,
    repository_data: RepositoryData,
) -> JsonReadingLogEntry:
    work = reading.work(repository_data.works)
    review = work.review(repository_data.reviews)

    return JsonReadingLogEntry(
        id=f"{reading.slug}-{timeline_index}",
        sequence=f"{reading.slug}-{timeline_index}",
        reviewSlug=review.slug if review else None,
        edition=reading.edition,
        kind=work.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        workYear=work.year,
        title=work.title,
        authors=[
            _build_json_reading_entry_author(work_author, repository_data.authors)
            for work_author in work.work_authors
        ],
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "timeline-entries")

    json_entries = [
        _build_json_reading_log_entry(
            reading=reading,
            timeline_entry=timeline_entry,
            repository_data=repository_data,
            timeline_index=timeline_index,
        )
        for reading in repository_data.readings
        for timeline_index, timeline_entry in enumerate(reading.timeline)
    ]

    grouped_entries = group_list_by_key(
        json_entries, lambda entry: f"{entry['date'].year}-{entry['date'].month:02}"
    )

    for year_month, entries in grouped_entries.items():
        exporter.serialize_dicts_to_file(
            dicts=sorted(entries, key=lambda entry: entry["sequence"]),
            folder_name="reading-log",
            file_name=year_month,
        )
