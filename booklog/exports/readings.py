import datetime
from typing import TypedDict

from booklog.bookdata.authors import Author
from booklog.bookdata.works import Work
from booklog.readings.reading import Reading
from booklog.utils import export_tools
from booklog.utils.logging import logger

TimelineEntry = TypedDict("TimelineEntry", {"date": datetime.date, "progress": str})

JsonAuthor = TypedDict(
    "JsonAuthor",
    {
        "name": str,
        "slug": str,
    },
)

JsonReading = TypedDict(
    "JsonReading",
    {
        "sequence": int,
        "workSlug": str,
        "title": str,
        "yearPublished": str,
        "edition": str,
        "authors": list[JsonAuthor],
    },
)


def export(
    readings: list[Reading],
    authors: list[Author],
    works: list[Work],
) -> None:
    logger.log("==== Begin exporting {}...", "readings")

    json_readings = []

    for reading in readings:
        reading_work = next(work for work in works if work.slug == reading.work_slug)
        reading_work_author_slugs = [
            work_author.slug for work_author in reading_work.authors
        ]
        reading_authors = [
            author for author in authors if author.slug in reading_work_author_slugs
        ]

        json_readings.append(
            JsonReading(
                sequence=reading.sequence,
                workSlug=reading.work_slug,
                title=reading_work.title,
                yearPublished=reading_work.year,
                edition=reading.edition,
                authors=[
                    JsonAuthor(name=reading_author.name, slug=reading_author.slug)
                    for reading_author in reading_authors
                ],
            )
        )

    export_tools.serialize_dicts(json_readings, "new_readings")
