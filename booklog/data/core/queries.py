from __future__ import annotations

from typing import Optional, Tuple

from booklog.data.core import json_authors, json_works, orm


def all_authors_and_works() -> Tuple[list[orm.AuthorWithWorks], list[orm.Work]]:
    all_json_authors = json_authors.deserialize_all()
    all_json_works = json_works.deserialize_all()

    return (
        all_authors(all_json_authors=all_json_authors, all_json_works=all_json_works),
        all_works(all_json_authors=all_json_authors, all_json_works=all_json_works),
    )


def all_works(
    all_json_authors: Optional[list[json_authors.JsonAuthor]] = None,
    all_json_works: Optional[list[json_works.JsonWork]] = None,
) -> list[orm.Work]:
    all_json_authors = all_json_authors or json_authors.deserialize_all()
    all_json_works = all_json_works or json_works.deserialize_all()

    return [
        orm.hydrate_json_work(
            json_work=json_work,
            all_json_authors=all_json_authors,
            all_json_works=all_json_works,
        )
        for json_work in all_json_works
    ]


def all_authors(
    all_json_authors: Optional[list[json_authors.JsonAuthor]] = None,
    all_json_works: Optional[list[json_works.JsonWork]] = None,
) -> list[orm.AuthorWithWorks]:
    all_json_authors = all_json_authors or json_authors.deserialize_all()
    all_json_works = all_json_works or json_works.deserialize_all()

    return [
        orm.hydrate_json_author_with_works(
            json_author=json_author,
            all_json_works=all_json_works,
            all_json_authors=all_json_authors,
        )
        for json_author in all_json_authors
    ]


def search_authors(query: str) -> list[orm.AuthorWithWorks]:
    all_json_authors = json_authors.deserialize_all()
    all_json_works = json_works.deserialize_all()

    filtered_authors = filter(
        lambda json_author: query.lower() in json_author["name"].lower(),
        all_json_authors,
    )

    return [
        orm.hydrate_json_author_with_works(
            json_author=json_author,
            all_json_authors=all_json_authors,
            all_json_works=all_json_works,
        )
        for json_author in filtered_authors
    ]


def search_works(query: str) -> list[orm.Work]:
    all_json_authors = json_authors.deserialize_all()
    all_json_works = json_works.deserialize_all()

    filtered_works = filter(
        lambda json_work: query.lower()
        in "{0}: {1}".format(json_work["title"], json_work["subtitle"]).lower(),
        all_json_works,
    )

    return [
        orm.hydrate_json_work(
            json_work=json_work,
            all_json_authors=all_json_authors,
            all_json_works=all_json_works,
        )
        for json_work in filtered_works
    ]
