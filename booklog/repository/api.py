from __future__ import annotations

import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, cast

from booklog.repository import json_authors, json_works, markdown_readings, markdown_reviews

WORK_KINDS = json_works.KINDS

Kind = json_works.Kind

SequenceError = markdown_readings.SequenceError

Grade = Literal[
    "A+", "A", "A-",
    "B+", "B", "B-",
    "C+", "C", "C-",
    "D+", "D", "D-",
    "F+", "F", "F-",
    "Abandoned"
]


@dataclass
class Author:
    name: str
    sort_name: str
    slug: str

    def works(self, cache: list[Work] | None = None) -> Iterable[Work]:
        works_iterable = cache or works()

        return filter(
            lambda work: self.slug
            in {work_author.author_slug for work_author in work.work_authors},
            works_iterable,
        )


@dataclass
class WorkAuthor:
    notes: str | None
    author_slug: str

    def author(self, cache: list[Author] | None = None) -> Author:
        author_iterable = cache or authors()
        author = next(
            (author for author in author_iterable if author.slug == self.author_slug),
            None
        )
        if not author:
            raise ValueError(f"Author with slug '{self.author_slug}' not found")
        return author


@dataclass
class Work:
    title: str
    subtitle: str | None
    year: str
    sort_title: str
    slug: str
    kind: Kind
    included_work_slugs: list[str]
    work_authors: list[WorkAuthor]

    def included_works(self, cache: list[Work] | None = None) -> Iterable[Work]:
        works_iterable = cache or works()
        return filter(
            lambda work: work.slug in self.included_work_slugs,
            works_iterable,
        )

    def included_in_works(self, cache: list[Work] | None = None) -> Iterable[Work]:
        works_iterable = cache or works()
        return filter(
            lambda work: self.slug in work.included_work_slugs,
            works_iterable,
        )

    def readings(self, cache: list[Reading] | None = None) -> Iterable[Reading]:
        readings_iterable = cache or readings()

        for reading in readings_iterable:
            if reading.work_slug == self.slug:
                yield reading

    def review(self, cache: list[Review] | None = None) -> Review | None:
        reviews_iterable = cache or reviews()
        return next(
            (review for review in reviews_iterable if review.work_slug == self.slug),
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
    edition_notes: str | None = None
    work_slug: str

    def work(self, cache: list[Work] | None = None) -> Work:
        works_iterable = cache or works()
        work = next(
            (work for work in works_iterable if work.slug == self.work_slug),
            None
        )
        if not work:
            raise ValueError(f"Work with slug '{self.work_slug}' not found")
        return work


@dataclass
class Review:
    work_slug: str
    date: datetime.date
    grade: Grade
    review_content: str | None = None

    def work(self, cache: list[Work] | None = None) -> Work:
        works_iterable = cache or works()
        work = next(
            (work for work in works_iterable if work.slug == self.work_slug),
            None
        )
        if not work:
            raise ValueError(f"Work with slug '{self.work_slug}' not found")
        return work

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


def works() -> Iterable[Work]:
    for json_work in json_works.read_all():
        yield _hydrate_json_work(json_work=json_work)


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


def create_work(
    title: str,
    subtitle: str | None,
    year: str,
    work_authors: list[WorkAuthor],
    kind: Kind,
    included_work_slugs: list[str] | None = None,
) -> Work:
    return _hydrate_json_work(
        json_work=json_works.create(
            title=title,
            subtitle=subtitle,
            year=year,
            work_authors=[
                json_works.CreateWorkAuthor(slug=work_author.author_slug, notes=work_author.notes)
                for work_author in work_authors
            ],
            kind=kind,
            included_work_slugs=included_work_slugs,
        ),
    )


def create_reading(
    work: Work,
    timeline: list[TimelineEntry],
    edition: str,
) -> Reading:
    return _hydrate_markdown_reading(
        markdown_reading=markdown_readings.create(
            work_slug=work.slug,
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
    work: Work,
    date: datetime.date,
    grade: Grade = "Abandoned",
) -> Review:
    return _hydrate_markdown_review(
        markdown_review=markdown_reviews.create_or_update(
            work_slug=work.slug,
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


def _hydrate_json_work(json_work: json_works.JsonWork) -> Work:
    return Work(
        title=json_work["title"],
        subtitle=json_work["subtitle"],
        sort_title=json_work["sortTitle"],
        slug=json_work["slug"],
        year=json_work["year"],
        kind=json_work["kind"],
        included_work_slugs=json_work["includedWorks"],
        work_authors=[
            WorkAuthor(author_slug=work_author["slug"], notes=work_author["notes"])
            for work_author in json_work["authors"]
        ],
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
        edition_notes=markdown_reading["edition_notes"],
        work_slug=markdown_reading["work_slug"],
    )


def _hydrate_markdown_review(
    markdown_review: markdown_reviews.MarkdownReview,
) -> Review:
    return Review(
        work_slug=markdown_review.yaml["work_slug"],
        date=markdown_review.yaml["date"],
        grade=cast(Grade, markdown_review.yaml["grade"]),
        review_content=markdown_review.review_content,
    )
