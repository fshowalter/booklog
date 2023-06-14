import datetime
from typing import TypedDict

from booklog.readings import serializer
from booklog.reviews import serializer as reviews_serializer
from booklog.utils import export_tools
from booklog.utils.logging import logger

JsonProgress = TypedDict(
    "JsonProgress",
    {
        "sequence": int,
        "workSlug": str,
        "edition": str,
        "date": datetime.date,
        "progress": str,
        "reviewed": bool,
        "readingYear": int,
    },
)


def export() -> None:
    logger.log("==== Begin exporting {}...", "progress")

    reviewed_work_slugs = {
        review.work_slug for review in reviews_serializer.deserialize_all()
    }

    json_progress = [
        JsonProgress(
            sequence=reading.sequence,
            workSlug=reading.work_slug,
            edition=reading.edition,
            date=entry.date,
            progress=entry.progress,
            reviewed=reading.work_slug in reviewed_work_slugs,
            readingYear=entry.date.year,
        )
        for reading in serializer.deserialize_all()
        for entry in reading.timeline
    ]

    export_tools.serialize_dicts(json_progress, "progress")
