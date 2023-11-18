from __future__ import annotations

from booklog.data.core import json_authors, json_works, orm


def all_works() -> list[orm.Work]:
    return [
        orm.hydrate_json_work(json_work=json_work)
        for json_work in json_works.deserialize_all()
    ]


def all_authors() -> list[orm.AuthorWithWorks]:
    return [
        orm.hydrate_json_author_with_works(json_author=json_author)
        for json_author in json_authors.deserialize_all()
    ]


def search_authors(query: str) -> list[orm.AuthorWithWorks]:
    filtered_authors = filter(
        lambda json_author: query.lower() in json_author["name"].lower(),
        json_authors.deserialize_all(),
    )

    return [
        orm.hydrate_json_author_with_works(json_author=json_author)
        for json_author in filtered_authors
    ]


def search_works(query: str) -> list[orm.Work]:
    filtered_works = filter(
        lambda json_work: query.lower()
        in "{0}: {1}".format(json_work["title"], json_work["subtitle"]).lower(),
        json_works.deserialize_all(),
    )

    return [orm.hydrate_json_work(json_work=json_work) for json_work in filtered_works]


# def author_names_for_work(work: Work) -> list[str]:
#     author_slugs = list(map(lambda author: author.slug, work.authors))

#     filtered_authors = filter(lambda author: author.slug in author_slugs, all_authors())

#     return list(map(lambda author: author.name, filtered_authors))


# def author_for_slug(author_slug: str) -> orm.Author:
#     return next(author for author in all_authors() if author.slug == author_slug)


# def works_for_author(author_slug: str) -> list[Work]:
#     return list(
#         filter(
#             lambda work: author_slug in set(author.slug for author in work.authors),
#             all_works(),
#         )
#     )
