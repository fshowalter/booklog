import datetime
from typing import Callable, Optional, TypedDict, TypeVar

from booklog.exports import exporter, json_work_author
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger

JsonTimelineEntry = TypedDict(
    "JsonTimelineEntry",
    {"date": datetime.date, "progress": str},
)

JsonMoreReviewEntryAuthor = TypedDict(
    "JsonMoreReviewEntryAuthor",
    {
        "name": str,
    },
)


JsonReading = TypedDict(
    "JsonReading",
    {
        "date": datetime.date,
        "edition": str,
        "editionNotes": Optional[str],
        "isAudiobook": bool,
        "readingTime": int,
        "abandoned": bool,
        "sequence": int,
        "timeline": list[JsonTimelineEntry],
    },
)

JsonMoreReviewEntry = TypedDict(
    "JsonMoreReviewEntry",
    {
        "title": str,
        "yearPublished": str,
        "kind": str,
        "authors": list[JsonMoreReviewEntryAuthor],
        "grade": str,
        "slug": str,
    },
)

JsonMoreByAuthorEntry = TypedDict(
    "JsonMoreByAuthorEntry",
    {"name": str, "slug": str, "works": list[JsonMoreReviewEntry]},
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
        "moreReviews": list[JsonMoreReviewEntry],
        "moreByAuthors": list[JsonMoreByAuthorEntry],
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
        isAudiobook=reading.edition == "Audible",
        abandoned=last_timeline_entry.progress == "Abandoned",
        readingTime=reading_time,
        timeline=[
            JsonTimelineEntry(
                date=timeline_entry.date, progress=timeline_entry.progress
            )
            for timeline_entry in reading.timeline
        ],
    )


def build_json_more_review_entry(
    work: repository_api.Work, repository_data: RepositoryData
) -> JsonMoreReviewEntry:
    review = work.review(repository_data.reviews)

    assert review, "Expected review for {0}".format(work.title)

    return JsonMoreReviewEntry(
        title=work.title,
        kind=work.kind,
        yearPublished=work.year,
        slug=work.slug,
        grade=review.grade,
        authors=[
            JsonMoreReviewEntryAuthor(
                name=work_author.author(repository_data.authors).name,
            )
            for work_author in work.work_authors
        ],
    )


ListType = TypeVar("ListType")


def slice_collection(  # noqa: WPS210
    collection: list[ListType], matcher: Callable[[ListType], bool]
) -> list[ListType]:
    midpoint = next(
        index
        for index, collection_item in enumerate(collection)
        if matcher(collection_item)
    )

    collection_length = len(collection)

    start_index = midpoint - 2
    end_index = midpoint + 3

    if start_index >= 0 and end_index < collection_length:
        return collection[start_index:end_index]

    if start_index < 0:
        start_index += collection_length
    if end_index > collection_length:
        end_index -= collection_length

    return collection[start_index:] + collection[:end_index]


def build_more_reviews(
    work: repository_api.Work,
    more_by_author_entries: list[JsonMoreByAuthorEntry],
    repository_data: RepositoryData,
) -> list[JsonMoreReviewEntry]:
    slugs_to_exclude = [
        work_entry["slug"]
        for more_by_author_entry in more_by_author_entries
        for work_entry in more_by_author_entry["works"]
    ]

    sliced_reviews = slice_collection(
        collection=sorted(
            (
                review
                for review in repository_data.reviews
                if review.work_slug not in slugs_to_exclude
            ),
            key=lambda review: review.work(repository_data.works).sort_title,
        ),
        matcher=build_review_matcher(work.slug),
    )

    return [
        build_json_more_review_entry(
            work=review.work(repository_data.works), repository_data=repository_data
        )
        for review in sliced_reviews
        if review.work_slug != work.slug
    ]


def build_review_matcher(slug_to_match: str) -> Callable[[repository_api.Review], bool]:
    return lambda review: review.work_slug == slug_to_match


def build_work_matcher(slug_to_match: str) -> Callable[[repository_api.Work], bool]:
    return lambda work: work.slug == slug_to_match


def build_more_by_authors(
    work: repository_api.Work, repository_data: RepositoryData
) -> list[JsonMoreByAuthorEntry]:
    more_by_author_entries: list[JsonMoreByAuthorEntry] = []

    for work_author in work.work_authors:
        author = work_author.author(repository_data.authors)
        reviewed_author_works = list(
            author_work
            for author_work in author.works(repository_data.works)
            if author_work.review(repository_data.reviews) is not None
        )

        if len(reviewed_author_works) < 5:
            continue

        sliced_works = slice_collection(
            collection=sorted(
                reviewed_author_works,
                key=lambda reviewed_author_work: reviewed_author_work.year,
            ),
            matcher=build_work_matcher(work.slug),
        )

        more_by_author_entries.append(
            JsonMoreByAuthorEntry(
                name=author.name,
                slug=author.slug,
                works=[
                    build_json_more_review_entry(
                        work=author_work, repository_data=repository_data
                    )
                    for author_work in sliced_works
                    if author_work.slug != work.slug
                ],
            )
        )

    return more_by_author_entries


def build_json_reviewed_work(
    work: repository_api.Work,
    readings_for_work: list[repository_api.Reading],
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedWork:
    most_recent_reading = sorted(
        readings_for_work, key=lambda reading: reading.sequence, reverse=True
    )[0]

    more_by_authors = build_more_by_authors(work=work, repository_data=repository_data)
    more_reviews = build_more_reviews(
        work=work,
        more_by_author_entries=more_by_authors,
        repository_data=repository_data,
    )

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
        moreByAuthors=more_by_authors,
        moreReviews=more_reviews,
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