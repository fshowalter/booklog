from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from glob import glob
from typing import Any, Optional

from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "works"

KINDS = set(
    [
        "Anthology",
        "Collection",
        "Nonfiction",
        "Novel",
        "Novella",
        "Short Story",
    ]
)


@dataclass
class WorkAuthor(object):
    slug: str
    notes: Optional[str]


@dataclass
class Work(object):
    title: str
    subtitle: Optional[str]
    year: str
    sort_title: str
    authors: list[WorkAuthor]
    slug: str
    kind: str

    @property
    def full_title(self) -> str:
        if self.subtitle:
            return "{0}: {1}".format(self.title, self.subtitle)

        return self.title


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


def create(
    title: str, subtitle: Optional[str], year: str, authors: list[WorkAuthor], kind: str
) -> Work:
    slug = slugify(
        "{0}-by-{1}".format(
            title.replace("'", ""), ", ".join(author.slug for author in authors)
        )
    )

    work = Work(
        title=title,
        subtitle=subtitle,
        sort_title=generate_sort_title(title, subtitle),
        year=year,
        authors=authors,
        slug=slug,
        kind=kind,
    )

    serialize(work)

    return work


def deserialize_json_work(json_work: dict[str, Any]) -> Work:
    authors = []

    for json_work_author in json_work["authors"]:
        authors.append(
            WorkAuthor(slug=json_work_author["slug"], notes=json_work_author["notes"])
        )

    return Work(
        title=json_work["title"],
        subtitle=json_work["subtitle"],
        sort_title=json_work["sort_title"],
        year=json_work["year"],
        authors=authors,
        slug=json_work["slug"],
        kind=json_work["kind"],
    )


def deserialize_all() -> list[Work]:
    works: list[Work] = []

    for file_path in glob(os.path.join(FOLDER_NAME, "*.json")):
        with open(file_path, "r") as json_file:
            works.append(deserialize_json_work(json.load(json_file)))

    return works


def works_for_author(author_slug: str) -> list[Work]:
    all_works = deserialize_all()

    return list(
        filter(
            lambda work: author_slug in set(author.slug for author in work.authors),
            all_works,
        )
    )


def serialize(work: Work) -> None:
    file_path = os.path.join(FOLDER_NAME, "{0}.json".format(work.slug))
    path_tools.ensure_file_path(file_path)

    with open(file_path, "w") as output_file:
        output_file.write(json.dumps(asdict(work), default=str, indent=2))

    logger.log(
        "Wrote {}.",
        file_path,
    )


def all_kinds() -> set[str]:
    return set()
