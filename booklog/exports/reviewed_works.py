import datetime
from collections.abc import Callable, Iterable
from itertools import count
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonWorkAuthor(TypedDict):
    notes: str | None
    name: str
    slug: str
    sortName: str


class JsonMoreByAuthor(TypedDict):
    author: str
    reviews: list[str]


class JsonReviewedWork(TypedDict):
    id: str
    reviewSequence: str
    grade: str
    reviewDate: datetime.date
    title: str
    sortTitle: str
    subtitle: str | None
    workYear: str
    authors: list[JsonWorkAuthor]
    kind: str
    review: str
    includedInWorks: list[str]
    includedWorks: list[str]
    moreReviews: list[str]
    moreByAuthors: list[JsonMoreByAuthor]


def _slice_list[ListType](
    source_list: list[ListType],
    matcher: Callable[[ListType], bool],
) -> list[ListType]:

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
    more_by_author_entries: list[JsonMoreByAuthor],
    repository_data: RepositoryData,
) -> list[str]:
    slugs_to_exclude = [
        slug
        for more_by_author_entry in more_by_author_entries
        for slug in more_by_author_entry["reviews"]
    ]

    sliced_reviews = _slice_list(
        source_list=sorted(
            (review for review in repository_data.reviews if review.slug not in slugs_to_exclude),
            key=lambda review: review.work(repository_data.works).sort_title,
        ),
        matcher=_build_review_matcher(work.slug),
    )

    return [review.slug for review in sliced_reviews if review.slug != work.slug]


def _build_review_matcher(
    slug_to_match: str,
) -> Callable[[repository_api.Review], bool]:
    return lambda review: review.slug == slug_to_match


def _build_work_matcher(slug_to_match: str) -> Callable[[repository_api.Work], bool]:
    return lambda work: work.slug == slug_to_match


def _build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)

    return JsonWorkAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        notes=work_author.notes,
    )


def _build_more_by_authors(
    work: repository_api.Work,
    repository_data: RepositoryData,
) -> list[JsonMoreByAuthor]:
    more_by_author_entries: list[JsonMoreByAuthor] = []

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
            JsonMoreByAuthor(
                author=author.slug,
                reviews=[
                    author_work.slug
                    for author_work in sliced_works
                    if author_work.slug != work.slug
                ],
            )
        )

    return more_by_author_entries


def _build_json_included_works(
    works: Iterable[repository_api.Work],
    repository_data: RepositoryData,
) -> list[str]:
    included_works = []

    for included_work in works:
        review = included_work.review(repository_data.reviews)

        if not review:
            continue

        included_works.append(included_work.slug)

    return included_works


def _build_json_reviewed_work(
    work: repository_api.Work,
    readings_for_work: list[repository_api.Reading],
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedWork:
    more_by_authors = _build_more_by_authors(work=work, repository_data=repository_data)
    more_reviews = _build_more_reviews(
        work=work,
        more_by_author_entries=more_by_authors,
        repository_data=repository_data,
    )

    most_recent_reading = sorted(readings_for_work, key=lambda reading: reading.slug, reverse=True)[
        0
    ]

    return JsonReviewedWork(
        id=work.slug,
        title=work.title,
        sortTitle=work.sort_title,
        subtitle=work.subtitle,
        workYear=work.year,
        kind=work.kind,
        review=review.slug,
        reviewDate=review.date,
        grade=review.grade,
        reviewSequence=f"{most_recent_reading.date}-{most_recent_reading.sequence:02}",
        authors=[
            _build_json_work_author(work_author=work_author, all_authors=repository_data.authors)
            for work_author in work.work_authors
        ],
        includedWorks=_build_json_included_works(
            work.included_works(repository_data.works),
            repository_data=repository_data,
        ),
        includedInWorks=_build_json_included_works(
            work.included_in_works(repository_data.works),
            repository_data=repository_data,
        ),
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
            _build_json_reviewed_work(
                work=work,
                readings_for_work=readings_for_work,
                review=review,
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        json_reviewed_works,
        "reviewed-works",
        filename_key=lambda json_work: json_work["id"],
    )
