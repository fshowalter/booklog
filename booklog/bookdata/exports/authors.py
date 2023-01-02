from typing import TypedDict

from booklog.bookdata import authors
from booklog.utils import export_tools
from booklog.utils.logging import logger

Author = TypedDict(
    "Author",
    {
        "name": str,
        "sortName": str,
        "key": str,
        "shelf": bool,
    },
)


def export() -> None:
    logger.log("==== Begin exporting {}...", "authors")

    all_authors = [
        Author(
            name=author.name,
            sortName=author.sort_name,
            key=author.slug,
            shelf=author.shelf,
        )
        for author in authors.deserialize_all()
    ]

    export_tools.serialize_dicts(all_authors, "authors")
