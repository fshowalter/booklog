from typing import Optional, TypedDict

from booklog.bookdata.api import Author, WorkAuthor

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {"name": str, "sortName": str, "slug": str, "notes": Optional[str]},
)


def build_json_work_authors(
    work_authors: list[WorkAuthor], authors: list[Author]
) -> list[JsonWorkAuthor]:
    json_work_authors = []

    for work_author in work_authors:
        author = next(author for author in authors if author.slug in work_author.slug)

        json_work_authors.append(
            JsonWorkAuthor(
                slug=work_author.slug,
                notes=work_author.notes,
                name=author.name,
                sortName=author.sort_name,
            )
        )

    return json_work_authors
