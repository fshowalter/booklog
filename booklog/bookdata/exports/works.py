from typing import Optional, TypedDict

from booklog.bookdata import works
from booklog.utils import export_tools
from booklog.utils.logging import logger

WorkAuthor = TypedDict(
    "WorkAuthor",
    {
        "key": str,
        "notes": Optional[str],
    },
)


Work = TypedDict(
    "Work",
    {
        "title": str,
        "subtitle": Optional[str],
        "yearPublished": str,
        "sortTitle": str,
        "authors": list[WorkAuthor],
        "key": str,
        "kind": str,
        "includedWorks": list[str],
    },
)


def export() -> None:
    logger.log("==== Begin exporting {}...", "works")

    all_works = [
        Work(
            title=work.title,
            subtitle=work.subtitle,
            yearPublished=work.year,
            sortTitle=work.sort_title,
            key=work.slug,
            kind=work.kind,
            includedWorks=work.included_works,
            authors=[
                WorkAuthor(key=author.slug, notes=author.notes)
                for author in work.authors
            ],
        )
        for work in works.deserialize_all()
    ]

    export_tools.serialize_dicts(all_works, "works")
