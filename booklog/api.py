from __future__ import annotations

from typing import Optional, Sequence, TypedDict

from booklog.bookdata import api as bookdata_api
from booklog.reviews import api as reviews_api
from booklog.utils import export_tools

AuthorWithWorks = bookdata_api.AuthorWithWorks

WorkWithAuthors = bookdata_api.WorkWithAuthors

Work = bookdata_api.Work

WorkAuthor = bookdata_api.WorkAuthor

TimelineEntry = reviews_api.TimelineEntry

create_author = bookdata_api.create_author

search_authors = bookdata_api.search_authors

search_works = bookdata_api.search_works

create_work = bookdata_api.create_work

create_review = reviews_api.create

all_editions = reviews_api.all_editions

WORK_KINDS = bookdata_api.WORK_KINDS


class ExportedAuthor(TypedDict):
    name: str
    sort_name: str
    slug: str
    reviewed: bool


class ExportedWorkAuthor(TypedDict):
    slug: str
    notes: Optional[str]


class ExportedWork(TypedDict):
    title: str
    subtitle: Optional[str]
    year: str
    sort_title: str
    authors: list[ExportedWorkAuthor]
    slug: str
    kind: str
    reviewed: bool
    included_works: list[str]


def all_reviewed_work_slugs(all_reviews: Sequence[reviews_api.Review]) -> set[str]:
    return set(review.slug for review in all_reviews)


def all_reviewed_author_slugs(
    reviewed_work_slugs: set[str],
    all_works: list[bookdata_api.Work],
) -> set[str]:
    slugs = []

    for work in all_works:
        if work.slug in reviewed_work_slugs:
            for work_author in work.authors:
                slugs.append(work_author.slug)

    return set(slugs)


def export_data() -> None:
    all_reviews = reviews_api.all_reviews()
    all_works = bookdata_api.all_works()
    all_authors = bookdata_api.all_authors()

    reviewed_work_slugs = all_reviewed_work_slugs(all_reviews=all_reviews)
    reviewed_author_slugs = all_reviewed_author_slugs(
        reviewed_work_slugs=reviewed_work_slugs, all_works=all_works
    )

    export_authors(all_authors=all_authors, reviewed_author_slugs=reviewed_author_slugs)
    export_works(
        all_works=all_works,
        reviewed_work_slugs=reviewed_work_slugs,
    )


def export_authors(
    all_authors: list[bookdata_api.Author],
    reviewed_author_slugs: set[str],
) -> None:
    serializable_authors = []

    for author in all_authors:

        serializable_authors.append(
            ExportedAuthor(
                name=author.name,
                sort_name=author.sort_name,
                slug=author.slug,
                reviewed=author.slug in reviewed_author_slugs,
            )
        )

    export_tools.serialize_dicts(serializable_authors, "authors")


def export_works(
    all_works: list[bookdata_api.Work],
    reviewed_work_slugs: set[str],
) -> None:
    serializable_works = []

    for work in all_works:
        work_authors = []
        work_reviewed = work.slug in reviewed_work_slugs

        for work_author in work.authors:
            work_authors.append(
                ExportedWorkAuthor(
                    slug=work_author.slug,
                    notes=work_author.notes,
                )
            )

        serializable_works.append(
            ExportedWork(
                title=work.title,
                subtitle=work.subtitle,
                sort_title=work.sort_title,
                year=work.year,
                authors=work_authors,
                slug=work.slug,
                reviewed=work_reviewed,
                kind=work.kind,
                included_works=work.included_works,
            )
        )

    export_tools.serialize_dicts(serializable_works, "works")
