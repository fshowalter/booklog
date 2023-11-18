from __future__ import annotations

import datetime
import json
import os
import re
from dataclasses import asdict
from glob import glob
from typing import Optional, TypedDict, cast

from slugify import slugify

from booklog.data.readings.reading import Reading, TimelineEntry
from booklog.data.utils import path_tools
from booklog.logger import logger

FOLDER_NAME = "readings"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


class JsonTimeline(TypedDict):
    date: str
    progress: str


class JsonReading(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[JsonTimeline]
    edition_notes: Optional[str]


def deserialize_timeline(reading: JsonReading) -> list[TimelineEntry]:
    timeline = []

    for timeline_entry in reading["timeline"]:
        timeline.append(
            TimelineEntry(
                date=datetime.date.fromisoformat(timeline_entry["date"]),
                progress=timeline_entry["progress"],
            )
        )

    return timeline


def deserialize(file_path: str) -> Reading:
    with open(file_path, "r") as json_file:
        json_object = cast(JsonReading, json.load(json_file))

    timeline = deserialize_timeline(reading=json_object)

    return Reading(
        work_slug=json_object["work_slug"],
        sequence=json_object["sequence"],
        edition=json_object["edition"],
        edition_notes=json_object["edition_notes"],
        timeline=timeline,
    )


def deserialize_all() -> list[Reading]:
    file_paths = glob(os.path.join(FOLDER_NAME, "*.json"))

    return [deserialize(file_path) for file_path in sorted(file_paths)]


def generate_file_path(reading: Reading) -> str:
    file_name = slugify(
        "{0:04d} {1}".format(reading.sequence, reading.work_slug),
    )

    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def serialize(reading: Reading) -> str:
    file_path = generate_file_path(reading)

    with open(file_path, "w") as output_file:
        json.dump(asdict(reading), output_file, indent=4, default=str)

    logger.log("Wrote {}", file_path)

    return file_path
