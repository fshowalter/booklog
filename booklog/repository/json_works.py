from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict, cast, get_args

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "works"

Kind = Literal[
    "Anthology",
    "Collection",
    "Nonfiction",
    "Novel",
    "Novella",
    "Short Story",
]
KINDS = get_args(Kind)


class JsonWorkAuthor(TypedDict):
    slug: str
    notes: str | None


class JsonWork(TypedDict):
    title: str
    subtitle: str | None
    year: str
    sortTitle: str  # noqa: WPS115
    authors: list[JsonWorkAuthor]
    slug: str
    kind: Kind
    includedWorks: list[str]  # noqa: WPS115


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
class CreateWorkAuthor:
    slug: str
    notes: str | None


def create(  # noqa: WPS211
    title: str,
    subtitle: str | None,
    year: str,
    work_authors: list[CreateWorkAuthor],
    kind: Kind,
    included_work_slugs: list[str] | None = None,
) -> JsonWork:
    slug = slugify(
        "{}-by-{}".format(
            title.replace("'", ""),
            ", ".join(work_author.slug for work_author in work_authors),
        )
    )

    json_work = JsonWork(
        title=title,
        subtitle=subtitle,
        sortTitle=generate_sort_title(title, subtitle),
        year=year,
        authors=[
            JsonWorkAuthor(slug=work_author.slug, notes=work_author.notes)
            for work_author in work_authors
        ],
        slug=slug,
        kind=kind,
        includedWorks=included_work_slugs or [],
    )

    serialize(json_work)

    return json_work


def read_all() -> Iterable[JsonWork]:
    for file_path in Path(FOLDER_NAME).glob("*.json"):
        with Path.open(file_path) as json_file:
            yield (cast(JsonWork, json.load(json_file)))


def serialize(json_work: JsonWork) -> None:
    file_path = Path(FOLDER_NAME) / f"{json_work["slug"]}.json"
    path_tools.ensure_file_path(file_path)

    with Path.open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_work, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )
