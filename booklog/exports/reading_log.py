import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.list_tools import group_list_by_key
from booklog.utils.logging import logger


class JsonTitleAuthor(TypedDict):
    notes: str | None
    name: str


class JsonReadingLogEntry(TypedDict):
    sequence: str
    reviewSlug: str | None
    id: str
    edition: str
    date: datetime.date
    progress: str
    titleYear: str
    title: str
    kind: str
    authors: list[JsonTitleAuthor]


def _build_json_reading_entry_author(
    title_author: repository_api.TitleAuthor, authors: list[repository_api.Author]
) -> JsonTitleAuthor:
    author = title_author.author(authors)
    return JsonTitleAuthor(name=author.name, notes=title_author.notes)


def _build_json_reading_log_entry(
    reading: repository_api.Reading,
    timeline_entry: repository_api.TimelineEntry,
    timeline_index: int,
    repository_data: RepositoryData,
) -> JsonReadingLogEntry:
    title = reading.title(repository_data.titles)
    review = title.review(repository_data.reviews)

    return JsonReadingLogEntry(
        id=f"{reading.slug}-{timeline_index}",
        sequence=f"{timeline_entry.date.isoformat()}-{reading.slug}",
        reviewSlug=review.slug if review else None,
        edition=reading.edition,
        kind=title.kind,
        date=timeline_entry.date,
        progress=timeline_entry.progress,
        titleYear=title.year,
        title=title.title,
        authors=[
            _build_json_reading_entry_author(title_author, repository_data.authors)
            for title_author in title.title_authors
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
