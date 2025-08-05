from typing import TypedDict

from booklog.repository import api as repository_api


class JsonWorkAuthor(TypedDict):
    name: str
    sortName: str
    slug: str
    notes: str | None


def build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)
    assert author, f"Author not found for slug: {work_author.author_slug}"

    return JsonWorkAuthor(
        slug=author.slug,
        notes=work_author.notes,
        name=author.name,
        sortName=author.sort_name,
    )
