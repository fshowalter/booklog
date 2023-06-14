from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from glob import glob
from typing import Any

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "authors"


@dataclass
class Author(object):
    name: str
    sort_name: str
    slug: str


def generate_sort_name(name: str) -> str:
    split_name = name.split()
    last_name = split_name[-1]
    other_names = split_name[:-1]

    return "{0}, {1}".format(last_name, " ".join(other_names))


def create(
    name: str,
) -> Author:
    slug = slugify(name)

    author = Author(name=name, sort_name=generate_sort_name(name), slug=slug)

    serialize(author=author)

    return author


def deserialize_json_author(json_author: dict[str, Any]) -> Author:
    return Author(
        name=json_author["name"],
        sort_name=json_author["sort_name"],
        slug=json_author["slug"],
    )


def deserialize_all() -> list[Author]:
    authors: list[Author] = []

    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            authors.append(deserialize_json_author(json.load(json_file)))

    return authors


def serialize(author: Author) -> None:
    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(author.slug))
    path_tools.ensure_file_path(file_path)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(asdict(author), default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )
