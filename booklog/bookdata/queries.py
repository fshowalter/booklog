from __future__ import annotations

from dataclasses import dataclass

from booklog.bookdata import authors, works

Author = authors.Author
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


def author_for_slug(author_slug: str) -> Author:
    return next(author for author in all_authors() if author.slug == author_slug)


def works_for_author(author_slug: str) -> list[Work]:
    return list(
        filter(
            lambda work: author_slug in set(author.slug for author in work.authors),
            all_works(),
        )
    )


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
