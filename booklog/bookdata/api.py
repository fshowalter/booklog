from __future__ import annotations

from dataclasses import dataclass

from booklog.bookdata import authors, works

all_authors = authors.deserialize_all

all_works = works.deserialize_all

create_author = authors.create

create_work = works.create

WorkAuthor = works.WorkAuthor

Work = works.Work

Author = authors.Author


@dataclass
class AuthorWithWorks(object):
    name: str
    sort_name: str
    slug: str
    works: list[works.Work]


def search_authors(query: str) -> list[AuthorWithWorks]:
    filtered_authors = filter(
        lambda author: query.lower() in author.name.lower(), all_authors()
    )

    matching_authors: list[AuthorWithWorks] = []

    for filtered_author in filtered_authors:
        matching_authors.append(
            AuthorWithWorks(
                name=filtered_author.name,
                sort_name=filtered_author.sort_name,
                slug=filtered_author.slug,
                works=works.works_for_author(filtered_author.slug),
            )
        )

    return matching_authors
