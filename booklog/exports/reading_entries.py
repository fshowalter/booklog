import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.json_author import JsonAuthor
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonReadingEntry(TypedDict):
    readingEntrySequence: int
    slug: str
    edition: str
    readingEntryDate: datetime.date
    progress: str
    reviewed: bool
    workYear: str
    title: str
    kind: str
    authors: list[JsonAuthor]
    includedInSlugs: list[str]


def _build_json_reading_entry_author(
    work_author: repository_api.WorkAuthor, authors: list[repository_api.Author]
) -> JsonAuthor:
    author = work_author.author(authors)
    return JsonAuthor(name=author.name, sortName=author.sort_name, slug=author.slug)


def _build_json_reading_entry(
    reading: repository_api.Reading,
    reading_entry: repository_api.TimelineEntry,
    repository_data: RepositoryData,
) -> JsonReadingEntry:
    work = reading.work(repository_data.works)
    reviewed = bool(work.review(repository_data.reviews))

    # Create the key tuple for looking up the sequence number
    entry_key = (str(reading_entry.date), str(reading.timeline[-1].date), str(reading.sequence))

    return JsonReadingEntry(
        readingEntrySequence=repository_data.reading_entry_sequence_map.get(entry_key, 0),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        readingEntryDate=reading_entry.date,
        progress=reading_entry.progress,
        reviewed=reviewed,
        workYear=work.year,
        title=work.title,
        authors=[
            _build_json_reading_entry_author(work_author, repository_data.authors)
            for work_author in work.work_authors
        ],
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "timeline-entries")

    json_entries = [
        _build_json_reading_entry(
            reading=reading,
            reading_entry=reading_entry,
            repository_data=repository_data,
        )
        for reading in repository_data.readings
        for reading_entry in reading.timeline
    ]

    exporter.serialize_dicts(
        sorted(json_entries, key=lambda entry: entry["readingEntrySequence"], reverse=True),
        "reading-entries",
    )
