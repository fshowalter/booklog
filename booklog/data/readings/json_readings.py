from __future__ import annotations

import json
import os
import re
from glob import glob
from typing import Any, Optional, Sequence, TypedDict

from slugify import slugify

from booklog.data.utils import path_tools
from booklog.logger import logger

FOLDER_NAME = "readings"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


class JsonTimelineEntry(TypedDict):
    date: str
    progress: str


class JsonReading(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[JsonTimelineEntry]
    edition_notes: Optional[str]


def create(
    work_slug: str, timeline: list[JsonTimelineEntry], edition: str
) -> JsonReading:
    json_reading = JsonReading(
        sequence=next_sequence(deserialize_all()),
        work_slug=work_slug,
        edition=edition,
        timeline=timeline,
        edition_notes=None,
    )

    serialize(json_reading)

    return json_reading


class SequenceError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def next_sequence(existing_instances: Sequence[JsonReading]) -> int:
    next_sequence_number = len(existing_instances) + 1
    last_instance: Optional[JsonReading] = None

    if next_sequence_number > 1:
        last_instance = existing_instances[-1]

    if last_instance and (last_instance["sequence"] != (next_sequence_number - 1)):
        raise SequenceError(
            "Last item {0} has sequence {1} but next sequence is {2}".format(
                existing_instances[-1:],
                last_instance["sequence"],
                next_sequence_number,
            ),
        )

    return next_sequence_number


def deserialize_json_reading(json_reading: dict[str, Any]) -> JsonReading:
    return JsonReading(
        work_slug=json_reading["work_slug"],
        sequence=json_reading["sequence"],
        edition=json_reading["edition"],
        edition_notes=json_reading["edition_notes"],
        timeline=[
            JsonTimelineEntry(
                date=json_reading_entry["date"], progress=json_reading_entry["progress"]
            )
            for json_reading_entry in json_reading["timeline"]
        ],
    )


def deserialize_all() -> list[JsonReading]:
    readings: list[JsonReading] = []

    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            readings.append(deserialize_json_reading(json.load(json_file)))

    return readings


def generate_file_path(json_reading: JsonReading) -> str:
    file_name = slugify(
        "{0:04d} {1}".format(json_reading["sequence"], json_reading["work_slug"]),
    )

    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def serialize(json_reading: JsonReading) -> str:
    file_path = generate_file_path(json_reading)

    with open(file_path, "w") as output_file:
        json.dump(json_reading, output_file, indent=4, default=str)

    logger.log("Wrote {}", file_path)

    return file_path
