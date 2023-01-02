import datetime
from typing import Optional, TypedDict

from booklog.readings import serializer
from booklog.readings.reading import Reading
from booklog.utils import export_tools
from booklog.utils.logging import logger

TimelineEntry = TypedDict("TimelineEntry", {"date": datetime.date, "progress": str})


JsonReading = TypedDict(
    "JsonReading",
    {
        "sequence": int,
        "workSlug": str,
        "edition": str,
        "timeline": list[TimelineEntry],
        "editionNotes": Optional[str],
    },
)


def export(readings: list[Reading]) -> None:
    logger.log("==== Begin exporting {}...", "readings")

    json_readings = [
        JsonReading(
            sequence=reading.sequence,
            workSlug=reading.work_slug,
            edition=reading.edition,
            editionNotes=reading.edition_notes,
            timeline=[
                TimelineEntry(date=entry.date, progress=entry.progress)
                for entry in reading.timeline
            ],
        )
        for reading in serializer.deserialize_all()
    ]

    export_tools.serialize_dicts(json_readings, "readings")
