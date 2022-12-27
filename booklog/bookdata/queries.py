from __future__ import annotations

from dataclasses import dataclass

from booklog.bookdata import authors, works

Work = works.Work
all_authors = authors.deserialize_all
all_works = works.deserialize_all


@dataclass
class AuthorWithWorks(object):
    name: str
    sort_name: str
    slug: str
    works: list[works.Work]


@dataclass
class WorkWithAuthors(object):
    title: str
    slug: str
    author_names: list[str]


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


def author_names_for_work(work: Work) -> list[str]:
    author_slugs = list(map(lambda author: author.slug, work.authors))

    filtered_authors = filter(lambda author: author.slug in author_slugs, all_authors())

    return list(map(lambda author: author.name, filtered_authors))


def search_works(query: str) -> list[WorkWithAuthors]:
    filtered_works = filter(
        lambda work: query.lower() in work.full_title.lower(), all_works()
    )

    matching_works: list[WorkWithAuthors] = []

    for filtered_work in filtered_works:

        matching_works.append(
            WorkWithAuthors(
                title=filtered_work.title,
                slug=filtered_work.slug,
                author_names=author_names_for_work(filtered_work),
            )
        )

    return matching_works
