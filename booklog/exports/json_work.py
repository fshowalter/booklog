from typing import TypedDict

from booklog.exports.json_work_author import JsonWorkAuthor


class JsonWork(TypedDict):
    title: str
    subtitle: str | None
    sortTitle: str
    workYear: str
    workYearSequence: int
    authorSequence: int
    titleSequence: int
    authors: list[JsonWorkAuthor]
    kind: str
    slug: str
    includedInSlugs: list[str]
