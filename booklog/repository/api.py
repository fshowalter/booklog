from __future__ import annotations

import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, cast

from booklog.repository import json_authors, json_titles, markdown_readings, markdown_reviews
from booklog.repository.types import NonEmptyList

TITLE_KINDS = json_titles.KINDS

Kind = json_titles.Kind

SequenceError = markdown_readings.SequenceError

Grade = Literal[
    "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F+", "F", "F-", "Abandoned"
]


@dataclass
class Author:
    name: str
    sort_name: str
    slug: str

    def titles(self, cache: list[Title] | None = None) -> Iterable[Title]:
        titles_iterable = cache or titles()

        return filter(
            lambda title: (
                self.slug in {title_author.author_slug for title_author in title.title_authors}
            ),
            titles_iterable,
        )


@dataclass
class TitleAuthor:
    notes: str | None
    author_slug: str

    def author(self, cache: list[Author] | None = None) -> Author:
        author_iterable = cache or authors()
        author = next(
            (author for author in author_iterable if author.slug == self.author_slug), None
        )
        if not author:
            raise ValueError(f"Author with slug '{self.author_slug}' not found")
        return author


@dataclass
class Title:
    title: str
    subtitle: str | None
    year: str
    sort_title: str
    slug: str
    kind: Kind
    included_title_ids: list[str]
    title_authors: NonEmptyList[TitleAuthor]

    def included_titles(self, cache: list[Title] | None = None) -> Iterable[Title]:
        titles_iterable = cache or titles()
        return filter(
            lambda title: title.slug in self.included_title_ids,
            titles_iterable,
        )

    def included_in_titles(self, cache: list[Title] | None = None) -> Iterable[Title]:
        titles_iterable = cache or titles()
        return filter(
            lambda title: self.slug in title.included_title_ids,
            titles_iterable,
        )

    def readings(self, cache: list[Reading] | None = None) -> Iterable[Reading]:
        readings_iterable = cache or readings()

        for reading in readings_iterable:
            if reading.titleId == self.slug:
                yield reading

    def review(self, cache: list[Review] | None = None) -> Review | None:
        reviews_iterable = cache or reviews()
        return next(
            (review for review in reviews_iterable if review.slug == self.slug),
            None,
        )


@dataclass
class TimelineEntry:
    date: datetime.date
    progress: str


@dataclass(kw_only=True)
class Reading:
    sequence: int
    edition: str
    timeline: list[TimelineEntry]
    editionNotes: str | None = None  # noqa: N815
    slug: str
    titleId: str  # noqa: N815
    date: datetime.date

    def title(self, cache: list[Title] | None = None) -> Title:
        titles_iterable = cache or titles()
        found = next((t for t in titles_iterable if t.slug == self.titleId), None)
        if not found:
            raise ValueError(f"Title with slug '{self.titleId}' not found")
        return found


@dataclass
class Review:
    slug: str
    date: datetime.date
    grade: Grade
    review_content: str | None = None

    def title(self, cache: list[Title] | None = None) -> Title:
        titles_iterable = cache or titles()
        found = next((t for t in titles_iterable if t.slug == self.slug), None)
        if not found:
            raise ValueError(f"Title with slug '{self.slug}' not found")
        return found

    @property
    def grade_value(self) -> int:
        if self.grade == "Abandoned":
            return 0

        value_modifier = 1

        grade_map = {
            "A": 12,
            "B": 9,
            "C": 6,
            "D": 3,
        }

        grade_value = grade_map.get(self.grade[0], 1)
        modifier = self.grade[-1]

        if modifier == "+":
            grade_value += value_modifier

        if modifier == "-":
            grade_value -= value_modifier

        return grade_value


def authors() -> Iterable[Author]:
    for json_author in json_authors.read_all():
        yield _hydrate_json_author(json_author=json_author)


def titles() -> Iterable[Title]:
    for json_title in json_titles.read_all():
        yield _hydrate_json_title(json_title=json_title)


def readings() -> Iterable[Reading]:
    for markdown_reading in markdown_readings.read_all():
        yield _hydrate_markdown_reading(markdown_reading=markdown_reading)


def reviews() -> Iterable[Review]:
    for markdown_review in markdown_reviews.read_all():
        yield _hydrate_markdown_review(markdown_review=markdown_review)


def reading_editions() -> set[str]:
    return {reading.edition for reading in readings()}


def create_author(
    name: str,
) -> Author:
    return _hydrate_json_author(json_authors.create(name=name))


def create_title(
    title: str,
    subtitle: str | None,
    year: str,
    title_authors: NonEmptyList[TitleAuthor],
    kind: Kind,
    included_title_ids: list[str] | None = None,
) -> Title:
    return _hydrate_json_title(
        json_title=json_titles.create(
            title=title,
            subtitle=subtitle,
            year=year,
            title_authors=[
                json_titles.CreateTitleAuthor(
                    slug=title_author.author_slug, notes=title_author.notes
                )
                for title_author in title_authors
            ],
            kind=kind,
            included_title_ids=included_title_ids,
        ),
    )


def create_reading(
    title: Title,
    timeline: list[TimelineEntry],
    edition: str,
) -> Reading:
    return _hydrate_markdown_reading(
        markdown_reading=markdown_readings.create(
            title_id=title.slug,
            timeline=[
                markdown_readings.TimelineEntry(
                    date=timeline_entry.date,
                    progress=timeline_entry.progress,
                )
                for timeline_entry in timeline
            ],
            edition=edition,
        ),
    )


def create_or_update_review(
    title: Title,
    date: datetime.date,
    grade: Grade = "Abandoned",
) -> Review:
    return _hydrate_markdown_review(
        markdown_review=markdown_reviews.create_or_update(
            title_id=title.slug,
            date=date,
            grade=grade,
        )
    )


def _hydrate_json_author(json_author: json_authors.JsonAuthor) -> Author:
    return Author(
        name=json_author["name"],
        slug=json_author["slug"],
        sort_name=json_author["sortName"],
    )


def _hydrate_json_title(json_title: json_titles.JsonTitle) -> Title:
    return Title(
        title=json_title["title"],
        subtitle=json_title["subtitle"],
        sort_title=json_title["sortTitle"],
        slug=json_title["slug"],
        year=json_title["year"],
        kind=json_title["kind"],
        included_title_ids=json_title["includedTitles"],
        title_authors=NonEmptyList.from_sequence(
            [
                TitleAuthor(author_slug=title_author["slug"], notes=title_author["notes"])
                for title_author in json_title["authors"]
            ]
        ),
    )


def _hydrate_markdown_reading(
    markdown_reading: markdown_readings.MarkdownReading,
) -> Reading:
    return Reading(
        sequence=markdown_reading["sequence"],
        timeline=[
            TimelineEntry(
                date=yaml_timeline_entry["date"],
                progress=yaml_timeline_entry["progress"],
            )
            for yaml_timeline_entry in markdown_reading["timeline"]
        ],
        edition=markdown_reading["edition"],
        editionNotes=markdown_reading["editionNotes"],
        slug=markdown_reading["slug"],
        titleId=markdown_reading["titleId"],
        date=markdown_reading["date"],
    )


def _hydrate_markdown_review(
    markdown_review: markdown_reviews.MarkdownReview,
) -> Review:
    return Review(
        slug=markdown_review.yaml["slug"],
        date=markdown_review.yaml["date"],
        grade=cast(Grade, markdown_review.yaml["grade"]),
        review_content=markdown_review.review_content,
    )
