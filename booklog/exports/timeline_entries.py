import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.json_author import JsonAuthor
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonTimelineEntry(TypedDict):
    timelineSequence: int
    slug: str
    edition: str
    timelineDate: datetime.date
    progress: str
    reviewed: bool
    workYear: str
    workYearSequence: int
    authorSequence: int
    titleSequence: int
    title: str
    kind: str
    authors: list[JsonAuthor]
    includedInSlugs: list[str]


def _build_json_timeline_entry_author(
    work_author: repository_api.WorkAuthor, authors: list[repository_api.Author]
) -> JsonAuthor:
    author = work_author.author(authors)
    return JsonAuthor(name=author.name, sortName=author.sort_name, slug=author.slug)


def _build_json_timeline_entry(
    reading: repository_api.Reading,
    timeline_entry: repository_api.TimelineEntry,
    repository_data: RepositoryData,
) -> JsonTimelineEntry:
    work = reading.work(repository_data.works)
    reviewed = bool(work.review(repository_data.reviews))

    # Create the key tuple for looking up the sequence number
    timeline_key = (str(timeline_entry.date), str(reading.timeline[-1].date), str(reading.sequence))

    return JsonTimelineEntry(
        timelineSequence=repository_data.timeline_sequence_map.get(timeline_key, 0),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        timelineDate=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        workYear=work.year,
        workYearSequence=repository_data.work_year_sequence_map.get(work.slug, 0),
        authorSequence=repository_data.author_sequence_map.get(work.slug, 0),
        titleSequence=repository_data.title_sequence_map.get(work.slug, 0),
        title=work.title,
        authors=[
            _build_json_timeline_entry_author(work_author, repository_data.authors)
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
        sorted(json_progress, key=lambda progress: progress["timelineSequence"]),
        "timeline-entries",
    )
