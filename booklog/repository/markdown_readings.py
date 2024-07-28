from __future__ import annotations

import datetime
import os
import re
from glob import glob
from typing import Any, Iterable, Optional, TypedDict, cast

import yaml
from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "readings"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


class TimelineEntry(TypedDict):
    date: datetime.date
    progress: str


class MarkdownReading(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: Optional[str]


def _represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "null")


def create(
    work_slug: str, timeline: list[TimelineEntry], edition: str
) -> MarkdownReading:
    new_reading = MarkdownReading(
        sequence=_next_sequence(),
        work_slug=work_slug,
        edition=edition,
        timeline=timeline,
        edition_notes=None,
    )

    _serialize(new_reading)

    return new_reading


class SequenceError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def _next_sequence() -> int:
    existing_instances = sorted(read_all(), key=lambda reading: reading["sequence"])
    next_sequence_number = len(existing_instances) + 1
    last_instance: Optional[MarkdownReading] = None

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


def read_all() -> Iterable[MarkdownReading]:
    for file_path in glob(os.path.join(FOLDER_NAME, "*.md")):
        with open(file_path, "r") as viewing_file:
            _, frontmatter, _notes = FM_REGEX.split(viewing_file.read(), 2)
            yield cast(MarkdownReading, yaml.safe_load(frontmatter))


def _generate_file_path(json_reading: MarkdownReading) -> str:
    file_name = slugify(
        "{0:04d} {1}".format(json_reading["sequence"], json_reading["work_slug"]),
    )

    file_path = os.path.join(FOLDER_NAME, "{0}.md".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def _serialize(markdown_reading: MarkdownReading) -> str:
    yaml.add_representer(type(None), _represent_none)

    file_path = _generate_file_path(markdown_reading)

    with open(file_path, "w") as markdown_file:
        markdown_file.write("---\n")
        yaml.dump(
            markdown_reading,
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            stream=markdown_file,
        )
        markdown_file.write("---\n\n")

    logger.log("Wrote {}.", file_path)

    return file_path
