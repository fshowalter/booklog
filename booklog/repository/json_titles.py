from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict, cast, get_args

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "titles"

Kind = Literal[
    "Anthology",
    "Collection",
    "Nonfiction",
    "Novel",
    "Novella",
    "Short Story",
]
KINDS = get_args(Kind)


class JsonTitleAuthor(TypedDict):
    slug: str
    notes: str | None


class JsonTitle(TypedDict):
    title: str
    subtitle: str | None
    year: str
    sortTitle: str
    authors: list[JsonTitleAuthor]
    slug: str
    kind: Kind
    includedTitles: list[str]


def generate_sort_title(title: str, subtitle: str | None) -> str:
    title_with_subtitle = title

    if subtitle:
        title_with_subtitle = f"{title}: {subtitle}"

    title_lower = title_with_subtitle.lower()
    title_words = title_with_subtitle.split(" ")
    lower_words = title_lower.split(" ")
    articles = {"a", "an", "the"}

    if (len(title_words) > 1) and (lower_words[0] in articles):
        return "{}".format(" ".join(title_words[1 : len(title_words)]))

    return title_with_subtitle


@dataclass
class CreateTitleAuthor:
    slug: str
    notes: str | None


def create(
    title: str,
    subtitle: str | None,
    year: str,
    title_authors: list[CreateTitleAuthor],
    kind: Kind,
    included_title_ids: list[str] | None = None,
) -> JsonTitle:
    slug = slugify(
        "{}-by-{}".format(
            title.replace("'", ""),
            ", ".join(title_author.slug for title_author in title_authors),
        )
    )

    json_title = JsonTitle(
        title=title,
        subtitle=subtitle,
        sortTitle=generate_sort_title(title, subtitle),
        year=year,
        authors=[
            JsonTitleAuthor(slug=title_author.slug, notes=title_author.notes)
            for title_author in title_authors
        ],
        slug=slug,
        kind=kind,
        includedTitles=included_title_ids or [],
    )

    serialize(json_title)

    return json_title


def read_all() -> Iterable[JsonTitle]:
    for file_path in Path(FOLDER_NAME).glob("*.json"):
        with Path.open(file_path) as json_file:
            yield (cast(JsonTitle, json.load(json_file)))


def serialize(json_title: JsonTitle) -> None:
    file_path = Path(FOLDER_NAME) / f"{json_title['slug']}.json"
    path_tools.ensure_file_path(file_path)

    with Path.open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_title, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )
