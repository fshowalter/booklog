import datetime
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.json_author import JsonAuthor
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


def _build_work_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{work.year}-{first_author_sort_name}-{work.sort_title}"


def _build_author_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{first_author_sort_name}-{work.year}-{work.sort_title}"


def _build_title_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{work.sort_title}-{first_author_sort_name}-{work.year}"


class JsonTimelineEntry(TypedDict):
    timelineSequence: str
    slug: str
    edition: str
    timelineDate: datetime.date
    progress: str
    reviewed: bool
    workYear: str
    workYearSequence: str
    authorSequence: str
    titleSequence: str
    title: str
    kind: str
    authors: list[JsonAuthor]
    includedInSlugs: list[str]


def _build_json_timeline_entry_author(
    work_author: repository_api.WorkAuthor,
    authors: list[repository_api.Author]
) -> JsonAuthor:
    author = work_author.author(authors)
    return JsonAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug
    )


def _build_json_timeline_entry(
    reading: repository_api.Reading,
    timeline_entry: repository_api.TimelineEntry,
    repository_data: RepositoryData,
) -> JsonTimelineEntry:
    work = reading.work(repository_data.works)
    reviewed = bool(work.review(repository_data.reviews))

    return JsonTimelineEntry(
        timelineSequence="{}-{}-{}".format(  # noqa: UP032,
            timeline_entry.date, reading.timeline[-1].date, reading.sequence
        ),
        slug=work.slug,
        edition=reading.edition,
        kind=work.kind,
        timelineDate=timeline_entry.date,
        progress=timeline_entry.progress,
        reviewed=reviewed,
        workYear=work.year,
        workYearSequence=_build_work_sequence(work, repository_data),
        authorSequence=_build_author_sequence(work, repository_data),
        titleSequence=_build_title_sequence(work, repository_data),
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
        sorted(json_progress, key=lambda progress: progress["timelineSequence"], reverse=True),
        "timeline-entries",
    )
