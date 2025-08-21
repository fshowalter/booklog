import datetime
from collections.abc import Callable
from itertools import count
from typing import TypedDict, TypeVar

from booklog.exports import exporter, json_work_author
from booklog.exports.json_author_with_reviewed_works import JsonAuthorWithReviewedWorks
from booklog.exports.json_maybe_reviewed_work import JsonMaybeReviewedWork
from booklog.exports.json_reviewed_work import JsonReviewedWork
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonReading(TypedDict):
    date: datetime.date
    isAudiobook: bool
    readingTime: int
    abandoned: bool
    readingSequence: int


class JsonReviewedWorkWithDetails(JsonReviewedWork):
    readings: list[JsonReading]
    moreReviews: list[JsonReviewedWork]
    moreByAuthors: list[JsonAuthorWithReviewedWorks]
    includedWorks: list[JsonMaybeReviewedWork]


def _build_json_reading(reading: repository_api.Reading) -> JsonReading:
    first_timeline_entry = sorted(reading.timeline, key=lambda entry: entry.date)[0]

    last_timeline_entry = sorted(reading.timeline, key=lambda entry: entry.date, reverse=True)[0]

    reading_time = (last_timeline_entry.date - first_timeline_entry.date).days + 1

    return JsonReading(
        readingSequence=reading.sequence,
        date=last_timeline_entry.date,
        isAudiobook=reading.edition == "Audible",
        abandoned=last_timeline_entry.progress == "Abandoned",
        readingTime=reading_time,
    )


def _build_json_more_review(
    work: repository_api.Work,
    repository_data: RepositoryData,
) -> JsonReviewedWork:
    review = work.review(repository_data.reviews)

    assert review, f"Expected review for {work.title}"

    return JsonReviewedWork(
        reviewSequence=repository_data.review_sequence_map.get(work.slug, 0),
        title=work.title,
        subtitle=work.subtitle,
        sortTitle=work.sort_title,
        kind=work.kind,
        workYear=work.year,
        workYearSequence=repository_data.work_year_sequence_map.get(work.slug, 0),
        authorSequence=repository_data.author_sequence_map.get(work.slug, 0),
        titleSequence=repository_data.title_sequence_map.get(work.slug, 0),
        slug=work.slug,
        grade=review.grade,
        gradeValue=review.grade_value,
        gradeSequence=repository_data.grade_sequence_map.get(work.slug, 0),
        reviewDate=review.date,
        yearReviewed=review.date.year,
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
        authors=[
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=repository_data.authors
            )
            for work_author in work.work_authors
        ],
    )


_ListType = TypeVar("_ListType")


def _slice_list(
    source_list: list[_ListType],
    matcher: Callable[[_ListType], bool],
) -> list[_ListType]:
    midpoint = next(
        index for index, collection_item in zip(count(), source_list) if matcher(collection_item)
    )

    start_index = midpoint - 3
    end_index = midpoint + 4

    if start_index >= 0 and end_index < len(source_list):
        return source_list[start_index:end_index]

    if start_index < 0:
        start_index += len(source_list)
    if end_index >= len(source_list):
        end_index -= len(source_list)

    return source_list[start_index:] + source_list[:end_index]


def _build_more_reviews(
    work: repository_api.Work,
    more_by_author_entries: list[JsonAuthorWithReviewedWorks],
    repository_data: RepositoryData,
) -> list[JsonReviewedWork]:
    slugs_to_exclude = [
        work_entry["slug"]
        for more_by_author_entry in more_by_author_entries
        for work_entry in more_by_author_entry["reviewedWorks"]
    ]

    sliced_reviews = _slice_list(
        source_list=sorted(
            (
                review
                for review in repository_data.reviews
                if review.work_slug not in slugs_to_exclude
            ),
            key=lambda review: review.work(repository_data.works).sort_title,
        ),
        matcher=_build_review_matcher(work.slug),
    )

    return [
        _build_json_more_review(
            work=review.work(repository_data.works),
            repository_data=repository_data,
        )
        for review in sliced_reviews
        if review.work_slug != work.slug
    ]


def _build_review_matcher(
    slug_to_match: str,
) -> Callable[[repository_api.Review], bool]:
    return lambda review: review.work_slug == slug_to_match


def _build_work_matcher(slug_to_match: str) -> Callable[[repository_api.Work], bool]:
    return lambda work: work.slug == slug_to_match


def _build_more_by_authors(
    work: repository_api.Work,
    repository_data: RepositoryData,
) -> list[JsonAuthorWithReviewedWorks]:
    more_by_author_entries: list[JsonAuthorWithReviewedWorks] = []

    for work_author in work.work_authors:
        author = work_author.author(repository_data.authors)
        reviewed_author_works = [
            author_work
            for author_work in author.works(repository_data.works)
            if author_work.review(repository_data.reviews) is not None
        ]

        if len(reviewed_author_works) < 5:
            continue

        sliced_works = _slice_list(
            source_list=sorted(
                reviewed_author_works,
                key=lambda reviewed_author_work: reviewed_author_work.year,
            ),
            matcher=_build_work_matcher(work.slug),
        )

        more_by_author_entries.append(
            JsonAuthorWithReviewedWorks(
                name=author.name,
                sortName=author.sort_name,
                slug=author.slug,
                reviewedWorks=[
                    _build_json_more_review(
                        work=author_work,
                        repository_data=repository_data,
                    )
                    for author_work in sliced_works
                    if author_work.slug != work.slug
                ],
            )
        )

    return more_by_author_entries


def _build_json_included_work(
    included_work: repository_api.Work,
    repository_data: RepositoryData,
) -> JsonMaybeReviewedWork:
    review = included_work.review(repository_data.reviews)

    return JsonMaybeReviewedWork(
        slug=included_work.slug,
        title=included_work.title,
        subtitle=included_work.subtitle,
        sortTitle=included_work.sort_title,
        grade=review.grade if review else None,
        gradeValue=review.grade_value if review else None,
        reviewDate=review.date if review else None,
        yearReviewed=review.date.year if review else None,
        kind=included_work.kind,
        workYear=included_work.year,
        workYearSequence=repository_data.work_year_sequence_map.get(included_work.slug, 0),
        authorSequence=repository_data.author_sequence_map.get(included_work.slug, 0),
        titleSequence=repository_data.title_sequence_map.get(included_work.slug, 0),
        authors=[
            json_work_author.build_json_work_author(
                work_author=included_work_author, all_authors=repository_data.authors
            )
            for included_work_author in included_work.work_authors
        ],
        includedInSlugs=[
            work.slug for work in included_work.included_in_works(repository_data.works)
        ],
    )


def _build_json_reviewed_work(
    work: repository_api.Work,
    readings_for_work: list[repository_api.Reading],
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedWorkWithDetails:
    more_by_authors = _build_more_by_authors(work=work, repository_data=repository_data)
    more_reviews = _build_more_reviews(
        work=work,
        more_by_author_entries=more_by_authors,
        repository_data=repository_data,
    )

    return JsonReviewedWorkWithDetails(
        reviewSequence=repository_data.review_sequence_map.get(work.slug, 0),
        slug=work.slug,
        title=work.title,
        subtitle=work.subtitle,
        sortTitle=work.sort_title,
        workYear=work.year,
        workYearSequence=repository_data.work_year_sequence_map.get(work.slug, 0),
        authorSequence=repository_data.author_sequence_map.get(work.slug, 0),
        titleSequence=repository_data.title_sequence_map.get(work.slug, 0),
        grade=review.grade,
        gradeValue=review.grade_value,
        gradeSequence=repository_data.grade_sequence_map.get(work.slug, 0),
        kind=work.kind,
        reviewDate=review.date,
        authors=[
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=repository_data.authors
            )
            for work_author in work.work_authors
        ],
        readings=[_build_json_reading(reading) for reading in readings_for_work],
        includedInSlugs=[
            included_in_work.slug
            for included_in_work in work.included_in_works(repository_data.works)
        ],
        yearReviewed=review.date.year,
        moreByAuthors=more_by_authors,
        moreReviews=more_reviews,
        includedWorks=[
            _build_json_included_work(
                included_work=included_work,
                repository_data=repository_data,
            )
            for included_work in work.included_works(repository_data.works)
        ],
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
            _build_json_reviewed_work(
                work=work,
                readings_for_work=readings_for_work,
                review=review,
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts(
        json_reviewed_works,
        "reviewed-works",
    )
