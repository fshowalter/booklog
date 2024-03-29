from __future__ import annotations

import json
import os
from dataclasses import dataclass
from glob import glob
from typing import Iterable, Literal, Optional, TypedDict, cast, get_args

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

JsonWorkAuthor = TypedDict(
    "JsonWorkAuthor",
    {
        "slug": str,
        "notes": Optional[str],
    },
)

JsonWork = TypedDict(
    "JsonWork",
    {
        "title": str,
        "subtitle": Optional[str],
        "year": str,
        "sortTitle": str,
        "authors": list[JsonWorkAuthor],
        "slug": str,
        "kind": Kind,
        "includedWorks": list[str],
    },
)


def generate_sort_title(title: str, subtitle: Optional[str]) -> str:
    title_with_subtitle = title

    if subtitle:
        title_with_subtitle = "{0}: {1}".format(title, subtitle)

    title_lower = title_with_subtitle.lower()
    title_words = title_with_subtitle.split(" ")
    lower_words = title_lower.split(" ")
    articles = set(["a", "an", "the"])

    if (len(title_words) > 1) and (lower_words[0] in articles):
        return "{0}".format(" ".join(title_words[1 : len(title_words)]))

    return title_with_subtitle


@dataclass
class CreateWorkAuthor:
    slug: str
    notes: Optional[str]


def create(  # noqa: WPS211
    title: str,
    subtitle: Optional[str],
    year: str,
    work_authors: list[CreateWorkAuthor],
    kind: Kind,
    included_work_slugs: Optional[list[str]] = None,
) -> JsonWork:
    slug = slugify(
        "{0}-by-{1}".format(
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
    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            yield (cast(JsonWork, json.load(json_file)))


def serialize(json_work: JsonWork) -> None:
    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(json_work["slug"]))
    path_tools.ensure_file_path(file_path)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(json_work, default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )
