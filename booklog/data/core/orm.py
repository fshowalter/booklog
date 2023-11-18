from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from booklog.data.core import json_authors, json_works


@dataclass
class Author(object):
    name: str
    sort_name: str
    slug: str


@dataclass
class AuthorWithWorks(Author):
    works: list[Work]


@dataclass
class WorkAuthor(Author):
    notes: Optional[str]


@dataclass
class Work(object):
    title: str
    subtitle: Optional[str]
    year: str
    sort_title: str
    authors: list[WorkAuthor]
    slug: str
    kind: str
    included_work_slugs: list[str]
    included_in_work_slugs: list[str]


def create_work(  # noqa: WPS211
    title: str,
    subtitle: Optional[str],
    year: str,
    work_authors: list[json_works.CreateWorkAuthor],
    kind: str,
    included_work_slugs: Optional[list[str]] = None,
) -> Work:
    return hydrate_json_work(
        json_works.create(
            title=title,
            subtitle=subtitle,
            year=year,
            work_authors=work_authors,
            kind=kind,
            included_work_slugs=included_work_slugs,
        )
    )


def create_author(
    name: str,
) -> Author:
    return hydrate_json_author(json_authors.create(name=name))


def hydrate_json_work_authors(
    json_work_authors: list[json_works.JsonWorkAuthor],
) -> list[WorkAuthor]:
    work_authors = []

    for work_author in json_work_authors:
        json_author = json_authors.author_for_slug(slug=work_author["slug"])
        work_authors.append(
            WorkAuthor(
                name=json_author["name"],
                slug=json_author["slug"],
                sort_name=json_author["sortName"],
                notes=work_author["notes"],
            )
        )

    return work_authors


def hydrate_json_work(json_work: json_works.JsonWork) -> Work:
    return Work(
        title=json_work["title"],
        subtitle=json_work["subtitle"],
        sort_title=json_work["sortTitle"],
        year=json_work["year"],
        authors=hydrate_json_work_authors(json_work["authors"]),
        slug=json_work["slug"],
        kind=json_work["kind"],
        included_work_slugs=json_work["includedWorks"],
        included_in_work_slugs=[
            collection_work["slug"]
            for collection_work in json_works.works_including_work_slug(
                json_work["slug"]
            )
        ],
    )


def hydrate_json_author(json_author: json_authors.JsonAuthor) -> Author:
    return Author(
        name=json_author["name"],
        slug=json_author["slug"],
        sort_name=json_author["sortName"],
    )


def hydrate_json_author_with_works(
    json_author: json_authors.JsonAuthor,
) -> AuthorWithWorks:
    return AuthorWithWorks(
        name=json_author["name"],
        slug=json_author["slug"],
        sort_name=json_author["sortName"],
        works=[
            hydrate_json_work(json_work)
            for json_work in json_works.works_for_author_slug(slug=json_author["slug"])
        ],
    )
