from typing import TypedDict

from booklog.bookdata import authors
from booklog.utils import export_tools
from booklog.utils.logging import logger

Author = TypedDict(
    "Author",
    {
        "name": str,
        "sortName": str,
        "slug": str,
    },
)


def export() -> None:
    logger.log("==== Begin exporting {}...", "authors")

    all_authors = [
        Author(
            name=author.name,
            sortName=author.sort_name,
            slug=author.slug,
        )
        for author in authors.deserialize_all()
    ]

    export_tools.serialize_dicts(all_authors, "authors")
