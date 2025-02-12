from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict, cast

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "authors"


class JsonAuthor(TypedDict):
    slug: str
    name: str
    sortName: str  # noqa: WPS115


def _generate_sort_name(name: str) -> str:
    split_name = name.split()
    last_name = split_name[-1]
    other_names = split_name[:-1]

    return "{}, {}".format(last_name, " ".join(other_names))


def create(name: str) -> JsonAuthor:
    json_author = JsonAuthor(
        name=name, sortName=_generate_sort_name(name=name), slug=slugify(name)
    )

    _serialize(json_author=json_author)

    return json_author


def read_all() -> Iterable[JsonAuthor]:
    for file_path in Path(FOLDER_NAME).glob("*.json"):
        with Path.open(file_path) as json_file:
            yield (cast(JsonAuthor, json.load(json_file)))


def _serialize(json_author: JsonAuthor) -> Path:
    file_path = Path(FOLDER_NAME) / f"{json_author["slug"]}.json"
    path_tools.ensure_file_path(file_path)

    with Path.open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_author, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )

    return file_path
