import datetime
import re
from collections import defaultdict
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, TypedDict, TypeVar, cast

import yaml

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "readings-new"
FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)

ListType = TypeVar("ListType")
KeyType = TypeVar("KeyType")


def group_list_by_key(
    iterable: Iterable[ListType], key: Callable[[ListType], KeyType]
) -> dict[KeyType, list[ListType]]:
    items_by_key = defaultdict(list)

    for iterable_item in iterable:
        items_by_key[key(iterable_item)].append(iterable_item)

    return items_by_key


class TimelineEntry(TypedDict):
    date: datetime.date
    progress: str


class MarkdownReading(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: str | None
    notes: str | None


class Frontmatter(TypedDict):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: str | None


def _represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "null")


def read_all() -> Iterable[MarkdownReading]:
    for file_path in Path("readings").glob("*.md"):
        with Path.open(file_path, "r") as viewing_file:
            _, frontmatter, notes = FM_REGEX.split(viewing_file.read(), 2)
            reading = cast(MarkdownReading, yaml.safe_load(frontmatter))
            reading["notes"] = notes
            yield reading


def rename_readings() -> None:
    existing_instances = sorted(read_all(), key=lambda reading: reading["sequence"])

    grouped_readings = group_list_by_key(
        existing_instances, lambda reading: reading["timeline"][-1]["date"]
    )

    for readings in grouped_readings.values():
        for index, reading in enumerate(readings):
            reading["sequence"] = index + 1
            _serialize(reading)


def _generate_file_path(markdown_reading: MarkdownReading) -> Path:
    file_name = "{}-{:02d}-{}".format(
        markdown_reading["timeline"][-1]["date"],
        markdown_reading["sequence"],
        markdown_reading["work_slug"],
    )

    file_path = Path(FOLDER_NAME) / f"{file_name}.md"

    path_tools.ensure_file_path(file_path)

    return file_path


def _serialize(markdown_reading: MarkdownReading) -> Path:
    yaml.add_representer(type(None), _represent_none)

    file_path = _generate_file_path(markdown_reading)

    frontmatter = Frontmatter(
        sequence=markdown_reading["sequence"],
        work_slug=markdown_reading["work_slug"],
        edition=markdown_reading["edition"],
        edition_notes=markdown_reading["edition_notes"],
        timeline=markdown_reading["timeline"],
    )

    with Path.open(file_path, "w") as markdown_file:
        markdown_file.write("---\n")
        yaml.dump(
            frontmatter,
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            stream=markdown_file,
        )
        markdown_file.write("---\n\n")
        if markdown_reading["notes"]:
            markdown_file.write(markdown_reading["notes"])

    logger.log("Wrote {}.", file_path)

    return file_path


if __name__ == "__main__":
    rename_readings()
    rename_readings()
