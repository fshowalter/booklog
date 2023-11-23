from typing import Optional, TypedDict

from booklog.repository import api as repository_api

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {"name": str, "sortName": str, "slug": str, "notes": Optional[str]},
)


def build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)

    return JsonWorkAuthor(
        slug=author.slug,
        notes=work_author.notes,
        name=author.name,
        sortName=author.sort_name,
    )
