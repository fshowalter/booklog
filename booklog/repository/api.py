from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Iterable, Optional

from booklog.repository import json_authors, json_readings, json_works, markdown_reviews

WORK_KINDS = json_works.KINDS

Kind = json_works.Kind

SequenceError = json_readings.SequenceError


@dataclass
class Author(object):
    name: str
    sort_name: str
    slug: str

    def works(self, cache: Optional[list[Work]] = None) -> Iterable[Work]:
        works_iterable = cache or works()

        return filter(
            lambda work: self.slug
            in {work_author.author_slug for work_author in work.work_authors},
            works_iterable,
        )


@dataclass
class WorkAuthor(object):
    notes: Optional[str]
    author_slug: str

    def author(self, cache: Optional[list[Author]] = None) -> Author:
        author_iterable = cache or authors()
        return next(
            author for author in author_iterable if author.slug == self.author_slug
        )


@dataclass
class Work(object):
    title: str
    subtitle: Optional[str]
    year: str
    sort_title: str
    slug: str
    kind: Kind
    included_work_slugs: list[str]
    work_authors: list[WorkAuthor]

    def included_works(self, cache: Optional[list[Work]] = None) -> Iterable[Work]:
        works_iterable = cache or works()
        return filter(
            lambda work: work.slug in self.included_work_slugs,
            works_iterable,
        )

    def included_in_works(self, cache: Optional[list[Work]] = None) -> Iterable[Work]:
        works_iterable = cache or works()
        return filter(
            lambda work: self.slug in work.included_work_slugs,
            works_iterable,
        )

    def readings(self, cache: Optional[list[Reading]] = None) -> Iterable[Reading]:
        readings_iterable = cache or readings()

        for reading in readings_iterable:
            if reading.work_slug == self.slug:
                yield reading

    def review(self, cache: Optional[list[Review]] = None) -> Optional[Review]:
        reviews_iterable = cache or reviews()
        return next(
            (review for review in reviews_iterable if review.work_slug == self.slug),
            None,
        )


@dataclass
class TimelineEntry(object):
    date: datetime.date
    progress: str


@dataclass(kw_only=True)
class Reading(object):
    sequence: int
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: Optional[str] = None
    work_slug: str

    def work(self, cache: Optional[list[Work]] = None) -> Work:
        works_iterable = cache or works()
        return next(work for work in works_iterable if work.slug == self.work_slug)


@dataclass
class Review(object):
    work_slug: str
    date: datetime.date
    grade: str
    review_content: Optional[str] = None

    def work(self, cache: Optional[list[Work]] = None) -> Work:
        works_iterable = cache or works()
        return next(work for work in works_iterable if work.slug == self.work_slug)

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
        yield hydrate_json_author(json_author=json_author)


def works() -> Iterable[Work]:
    for json_work in json_works.read_all():
        yield hydrate_json_work(json_work=json_work)


def readings() -> Iterable[Reading]:
    for json_reading in json_readings.read_all():
        yield hydrate_json_reading(json_reading=json_reading)


def reviews() -> Iterable[Review]:
    for markdown_review in markdown_reviews.read_all():
        yield hydrate_markdown_review(markdown_review=markdown_review)


def reading_editions() -> set[str]:
    return set([reading.edition for reading in readings()])


def create_author(
    name: str,
) -> Author:
    return hydrate_json_author(json_authors.create(name=name))


def create_work(  # noqa: WPS211
    title: str,
    subtitle: Optional[str],
    year: str,
    work_authors: list[WorkAuthor],
    kind: Kind,
    included_work_slugs: Optional[list[str]] = None,
) -> Work:
    return hydrate_json_work(
        json_work=json_works.create(
            title=title,
            subtitle=subtitle,
            year=year,
            work_authors=[
                json_works.CreateWorkAuthor(
                    slug=work_author.author_slug, notes=work_author.notes
                )
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
    return hydrate_json_reading(
        json_reading=json_readings.create(
            work_slug=work.slug,
            timeline=[
                json_readings.JsonTimelineEntry(
                    date=datetime.date.isoformat(timeline_entry.date),
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
    grade: str = "Abandoned",
) -> Review:
    return hydrate_markdown_review(
        markdown_review=markdown_reviews.create_or_update(
            work_slug=work.slug,
            date=date,
            grade=grade,
        )
    )


def hydrate_json_author(json_author: json_authors.JsonAuthor) -> Author:
    return Author(
        name=json_author["name"],
        slug=json_author["slug"],
        sort_name=json_author["sortName"],
    )


def hydrate_json_work(json_work: json_works.JsonWork) -> Work:
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


def hydrate_json_reading(json_reading: json_readings.JsonReading) -> Reading:
    return Reading(
        sequence=json_reading["sequence"],
        timeline=[
            TimelineEntry(
                date=datetime.date.fromisoformat(json_timeline_entry["date"]),
                progress=json_timeline_entry["progress"],
            )
            for json_timeline_entry in json_reading["timeline"]
        ],
        edition=json_reading["edition"],
        edition_notes=json_reading["edition_notes"],
        work_slug=json_reading["work_slug"],
    )


def hydrate_markdown_review(markdown_review: markdown_reviews.MarkdownReview) -> Review:
    return Review(
        work_slug=markdown_review.yaml["work_slug"],
        date=markdown_review.yaml["date"],
        grade=markdown_review.yaml["grade"],
        review_content=markdown_review.review_content,
    )
