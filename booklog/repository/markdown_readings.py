from __future__ import annotations

import datetime
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypedDict, cast

import yaml

from booklog.utils import list_tools, path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "readings"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


class BlockCollectionIndentDumper(yaml.Dumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, indentless=False)


class TimelineEntry(TypedDict):
    date: datetime.date
    progress: str


class MarkdownReading(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    edition_notes: str | None
    timeline: list[TimelineEntry]


def _represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "null")


def create(work_slug: str, timeline: list[TimelineEntry], edition: str) -> MarkdownReading:
    new_reading = MarkdownReading(
        sequence=_next_sequence_for_date(timeline[0]["date"]),
        work_slug=work_slug,
        edition=edition,
        edition_notes=None,
        timeline=timeline,
    )

    _serialize(new_reading)

    return new_reading


class SequenceError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def _next_sequence_for_date(date: datetime.date) -> int:
    existing_instances = sorted(
        read_all(),
        key=lambda reading: "{}-{}".format(reading["timeline"][-1]["date"], reading["sequence"]),
    )

    grouped_readings = list_tools.group_list_by_key(
        existing_instances, lambda reading: reading["timeline"][-1]["date"]
    )

    if date not in grouped_readings:
        return 1

    return len(grouped_readings[date]) + 1


def read_all() -> Iterable[MarkdownReading]:
    for file_path in Path(FOLDER_NAME).glob("*.md"):
        with Path.open(file_path) as viewing_file:
            _, frontmatter, _notes = FM_REGEX.split(viewing_file.read(), 2)
            yield cast(MarkdownReading, yaml.safe_load(frontmatter))


def _generate_file_path(json_reading: MarkdownReading) -> Path:
    file_name = "{}-{:02d}-{}".format(
        json_reading["timeline"][-1]["date"],
        json_reading["sequence"],
        json_reading["work_slug"],
    )

    file_path = Path(FOLDER_NAME) / f"{file_name}.md"

    path_tools.ensure_file_path(file_path)

    return file_path


def _serialize(markdown_reading: MarkdownReading) -> Path:
    yaml.add_representer(type(None), _represent_none)

    file_path = _generate_file_path(markdown_reading)

    with Path.open(file_path, "w") as markdown_file:
        markdown_file.write("---\n")
        yaml.dump(
            markdown_reading,
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            stream=markdown_file,
            Dumper=BlockCollectionIndentDumper,
        )
        markdown_file.write("---\n\n")

    logger.log("Wrote {}.", file_path)

    return file_path
