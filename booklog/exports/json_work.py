from typing import TypedDict

from booklog.exports.json_work_author import JsonWorkAuthor


class JsonWork(TypedDict):
    title: str
    subtitle: str | None
    sortTitle: str
    yearPublished: str
    authors: list[JsonWorkAuthor]
    kind: str
    slug: str
    includedInSlugs: list[str]
