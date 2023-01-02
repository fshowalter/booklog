from __future__ import annotations

import datetime
import os
import re
from glob import glob
from typing import Any, Optional, TypedDict, cast

import yaml

from booklog.reviews.review import Review
from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "reviews"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


class ReviewYaml(TypedDict):
    work_slug: str
    grade: Optional[str]
    date: datetime.date


def deserialize(file_path: str) -> Review:
    with open(file_path, "r") as review_file:
        _, frontmatter, review_content = FM_REGEX.split(review_file.read(), 2)

    review_yaml = cast(ReviewYaml, yaml.safe_load(frontmatter))

    return Review(
        grade=review_yaml["grade"],
        work_slug=review_yaml["work_slug"],
        date=review_yaml["date"],
        review_content=review_content,
    )


def deserialize_all() -> list[Review]:
    reviews: list[Review] = []
    for review_file_path in glob(os.path.join(FOLDER_NAME, "*.md")):
        reviews.append(deserialize(review_file_path))

    reviews.sort(key=lambda review: review.date)

    return reviews


def generate_file_path(review: Review) -> str:
    file_path = os.path.join(FOLDER_NAME, "{0}.md".format(review.work_slug))

    path_tools.ensure_file_path(file_path)

    return file_path


def generate_yaml(review: Review) -> ReviewYaml:
    return ReviewYaml(work_slug=review.work_slug, grade=review.grade, date=review.date)


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
