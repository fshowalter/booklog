from __future__ import annotations

import datetime
import os
import re
from glob import glob
from typing import Any, Optional, Sequence, TypedDict, cast

import yaml
from slugify import slugify

from booklog.reviews.review import ProgressMark, Review
from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "reviews"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


class ProgressYaml(TypedDict):
    date: datetime.date
    percent: int


class ReviewYaml(TypedDict):
    sequence: int
    slug: str
    grade: str
    edition: str
    progress: list[ProgressYaml]
    edition_notes: Optional[str]
    isbn: Optional[str]


def deserialize_progress(review_yaml: ReviewYaml) -> list[ProgressMark]:
    progress_marks = []

    for progress_yaml in review_yaml["progress"]:
        progress_marks.append(
            ProgressMark(date=progress_yaml["date"], percent=progress_yaml["percent"])
        )

    return progress_marks


def deserialize(file_path: str) -> Review:
    with open(file_path, "r") as review_file:
        _, frontmatter, review_content = FM_REGEX.split(review_file.read(), 2)

    review_yaml = cast(ReviewYaml, yaml.safe_load(frontmatter))

    progess = deserialize_progress(review_yaml=review_yaml)

    return Review(
        grade=review_yaml["grade"],
        slug=review_yaml["slug"],
        sequence=review_yaml["sequence"],
        edition=review_yaml["edition"],
        edition_notes=review_yaml["edition_notes"],
        isbn=review_yaml["isbn"],
        progress=progess,
        review_content=review_content,
    )


def deserialize_all() -> Sequence[Review]:
    reviews: list[Review] = []
    for review_file_path in glob(os.path.join(FOLDER_NAME, "*.md")):
        reviews.append(deserialize(review_file_path))

    reviews.sort(key=lambda review: review.sequence)

    return reviews


def generate_file_path(review: Review) -> str:
    file_name = slugify(
        "{0:04d} {1}".format(review.sequence, review.slug),
    )

    file_path = os.path.join(FOLDER_NAME, "{0}.md".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def generate_yaml(review: Review) -> ReviewYaml:
    return ReviewYaml(
        sequence=review.sequence,
        slug=review.slug,
        grade=review.grade,
        edition=review.edition,
        edition_notes=review.edition_notes,
        isbn=review.isbn,
        progress=[
            ProgressYaml(date=progress.date, percent=progress.percent)
            for progress in review.progress
        ],
    )


def serialize(review: Review) -> str:
    file_path = generate_file_path(review)

    stripped_content = str(review.review_content or "").strip()

    with open(file_path, "w") as output_file:
        output_file.write("---\n")
        yaml.dump(
            generate_yaml(review),
            encoding="utf-8",
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            stream=output_file,
        )
        output_file.write("---\n\n")
        output_file.write(stripped_content)

    logger.log("Wrote {}", file_path)

    return file_path
