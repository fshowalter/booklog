from __future__ import annotations

import json
import os
from glob import glob
from typing import Iterable, TypedDict, cast

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "authors"


JsonAuthor = TypedDict(
    "JsonAuthor",
    {
        "slug": str,
        "name": str,
        "sortName": str,
    },
)


def _generate_sort_name(name: str) -> str:
    split_name = name.split()
    last_name = split_name[-1]
    other_names = split_name[:-1]

    return "{0}, {1}".format(last_name, " ".join(other_names))


def create(name: str) -> JsonAuthor:
    json_author = JsonAuthor(
        name=name, sortName=_generate_sort_name(name=name), slug=slugify(name)
    )

    _serialize(json_author=json_author)

    return json_author


def read_all() -> Iterable[JsonAuthor]:
    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            yield (cast(JsonAuthor, json.load(json_file)))


def _serialize(json_author: JsonAuthor) -> str:
    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(json_author["slug"]))
    path_tools.ensure_file_path(file_path)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_author, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )

    return file_path
