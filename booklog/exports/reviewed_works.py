import datetime
from typing import Optional, TypedDict

from booklog.exports import exporter, json_work_author
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger

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
        "subtitle": Optional[str],
        "sortTitle": str,
        "yearPublished": str,
        "authors": list[json_work_author.JsonWorkAuthor],
        "grade": str,
        "gradeValue": int,
        "kind": str,
        "date": datetime.date,
        "yearReviewed": int,
        "readings": list[JsonReading],
    },
)


def build_json_reading(reading: repository_api.Reading) -> JsonReading:
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
    work: repository_api.Work,
    readings_for_work: list[repository_api.Reading],
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedWork:
    most_recent_reading = sorted(
        readings_for_work, key=lambda reading: reading.sequence, reverse=True
    )[0]

    return JsonReviewedWork(
        sequence=most_recent_reading.sequence,
        slug=work.slug,
        title=work.title,
        subtitle=work.subtitle,
        sortTitle=work.sort_title,
        yearPublished=work.year,
        grade=review.grade,
        gradeValue=review.grade_value,
        kind=work.kind,
        date=review.date,
        authors=[
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=repository_data.authors
            )
            for work_author in work.work_authors
        ],
        readings=[build_json_reading(reading) for reading in readings_for_work],
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
        yearReviewed=review.date.year,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reviewed-works")

    json_reviewed_works = []

    for review in repository_data.reviews:
        work = review.work(repository_data.works)
        readings_for_work = list(work.readings(repository_data.readings))
        if not readings_for_work:
            continue

        json_reviewed_works.append(
            build_json_reviewed_work(
                work=work,
                readings_for_work=readings_for_work,
                review=review,
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        json_reviewed_works,
        "reviewed_works",
        filename_key=lambda work: work["slug"],
    )
