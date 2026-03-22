import datetime
from collections.abc import Callable, Iterable
from itertools import count
from typing import TypedDict

from booklog.exports import exporter
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


class JsonTitleAuthor(TypedDict):
    notes: str | None
    name: str
    slug: str
    sortName: str


class JsonMoreByAuthor(TypedDict):
    author: str
    reviews: list[str]


class JsonReviewedTitle(TypedDict):
    id: str
    reviewSequence: str
    grade: str
    reviewDate: datetime.date
    title: str
    sortTitle: str
    subtitle: str | None
    titleYear: str
    authors: list[JsonTitleAuthor]
    kind: str
    review: str
    includedInTitles: list[str]
    includedTitles: list[str]
    moreReviews: list[str]
    moreByAuthors: list[JsonMoreByAuthor]


def _slice_list[ListType](
    source_list: list[ListType],
    matcher: Callable[[ListType], bool],
) -> list[ListType]:
    if len(source_list) < 7:
        return []

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
    title: repository_api.Title,
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
            key=lambda review: review.title(repository_data.titles).sort_title,
        ),
        matcher=_build_review_matcher(title.slug),
    )

    return [review.slug for review in sliced_reviews if review.slug != title.slug]


def _build_review_matcher(
    slug_to_match: str,
) -> Callable[[repository_api.Review], bool]:
    return lambda review: review.slug == slug_to_match


def _build_title_matcher(slug_to_match: str) -> Callable[[repository_api.Title], bool]:
    return lambda title: title.slug == slug_to_match


def _build_json_title_author(
    title_author: repository_api.TitleAuthor, all_authors: list[repository_api.Author]
) -> JsonTitleAuthor:
    author = title_author.author(all_authors)

    return JsonTitleAuthor(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        notes=title_author.notes,
    )


def _build_more_by_authors(
    title: repository_api.Title,
    repository_data: RepositoryData,
) -> list[JsonMoreByAuthor]:
    more_by_author_entries: list[JsonMoreByAuthor] = []

    for title_author in title.title_authors:
        author = title_author.author(repository_data.authors)
        reviewed_author_titles = [
            author_title
            for author_title in author.titles(repository_data.titles)
            if author_title.review(repository_data.reviews) is not None
        ]

        sliced_titles = _slice_list(
            source_list=sorted(
                reviewed_author_titles,
                key=lambda reviewed_author_title: reviewed_author_title.year,
            ),
            matcher=_build_title_matcher(title.slug),
        )

        if not sliced_titles:
            continue

        more_by_author_entries.append(
            JsonMoreByAuthor(
                author=author.slug,
                reviews=[
                    author_title.slug
                    for author_title in sliced_titles
                    if author_title.slug != title.slug
                ],
            )
        )

    return more_by_author_entries


def _build_json_included_titles(
    titles: Iterable[repository_api.Title],
    repository_data: RepositoryData,
) -> list[str]:
    included_titles = []

    for included_title in titles:
        review = included_title.review(repository_data.reviews)

        if not review:
            continue

        included_titles.append(included_title.slug)

    return included_titles


def _build_json_reviewed_title(
    title: repository_api.Title,
    readings_for_title: list[repository_api.Reading],
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedTitle:
    more_by_authors = _build_more_by_authors(title=title, repository_data=repository_data)
    more_reviews = _build_more_reviews(
        title=title,
        more_by_author_entries=more_by_authors,
        repository_data=repository_data,
    )

    most_recent_reading = sorted(
        readings_for_title, key=lambda reading: reading.slug, reverse=True
    )[0]

    return JsonReviewedTitle(
        id=title.slug,
        title=title.title,
        sortTitle=title.sort_title,
        subtitle=title.subtitle,
        titleYear=title.year,
        kind=title.kind,
        review=review.slug,
        reviewDate=review.date,
        grade=review.grade,
        reviewSequence=f"{most_recent_reading.date}-{most_recent_reading.sequence:02}",
        authors=[
            _build_json_title_author(title_author=title_author, all_authors=repository_data.authors)
            for title_author in title.title_authors
        ],
        includedTitles=_build_json_included_titles(
            title.included_titles(repository_data.titles),
            repository_data=repository_data,
        ),
        includedInTitles=_build_json_included_titles(
            title.included_in_titles(repository_data.titles),
            repository_data=repository_data,
        ),
        moreByAuthors=more_by_authors,
        moreReviews=more_reviews,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "reviewed-titles")

    json_reviewed_titles = []

    for review in repository_data.reviews:
        title = review.title(repository_data.titles)
        readings_for_title = list(title.readings(repository_data.readings))

        json_reviewed_titles.append(
            _build_json_reviewed_title(
                title=title,
                readings_for_title=readings_for_title,
                review=review,
                repository_data=repository_data,
            )
        )

    exporter.serialize_dicts_to_folder(
        json_reviewed_titles,
        "reviewed-titles",
        filename_key=lambda json_title: json_title["id"],
    )
