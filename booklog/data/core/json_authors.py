from __future__ import annotations

import json
import os
from glob import glob
from typing import Any, TypedDict

from slugify import slugify

from booklog.data.utils import path_tools
from booklog.logger import logger

FOLDER_NAME = "authors"


JsonAuthor = TypedDict(
    "JsonAuthor",
    {
        "slug": str,
        "name": str,
        "sortName": str,
    },
)


def generate_sort_name(name: str) -> str:
    split_name = name.split()
    last_name = split_name[-1]
    other_names = split_name[:-1]

    return "{0}, {1}".format(last_name, " ".join(other_names))


def author_for_slug(slug: str, all_json_authors: list[JsonAuthor]) -> JsonAuthor:
    return next(author for author in all_json_authors if author["slug"] == slug)


def create(
    name: str,
) -> JsonAuthor:
    slug = slugify(name)

    json_author = JsonAuthor(name=name, sortName=generate_sort_name(name), slug=slug)

    serialize(json_author=json_author)

    return json_author


def deserialize_json_author(json_author: dict[str, Any]) -> JsonAuthor:
    return JsonAuthor(
        name=json_author["name"],
        sortName=json_author["sortName"],
        slug=json_author["slug"],
    )


def deserialize_all() -> list[JsonAuthor]:
    authors: list[JsonAuthor] = []

    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            authors.append(deserialize_json_author(json.load(json_file)))

    return authors


def serialize(json_author: JsonAuthor) -> None:
    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(json_author["slug"]))
    path_tools.ensure_file_path(file_path)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_author, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )
