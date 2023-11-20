from __future__ import annotations

import os
import re
from dataclasses import dataclass
from glob import glob
from typing import Any, Optional, TypedDict

import yaml

from booklog.data.utils import path_tools
from booklog.logger import logger

FOLDER_NAME = "reviews"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


@dataclass(kw_only=True)
class MarkdownReview(object):
    yaml: ReviewYaml
    review_content: Optional[str] = None


class ReviewYaml(TypedDict):
    work_slug: str
    grade: str
    date: str


def review_for_work_slug(
    work_slug: str, all_markdown_reviews: list[MarkdownReview]
) -> MarkdownReview:
    return next(
        markdown_review
        for markdown_review in all_markdown_reviews
        if markdown_review.yaml["work_slug"] == work_slug
    )


def create(
    work_slug: str,
    grade: str,
    date: str,
) -> MarkdownReview:
    markdown_review = MarkdownReview(
        yaml=ReviewYaml(
            work_slug=work_slug,
            grade=grade,
            date=date,
        )
    )

    serialize(markdown_review)

    return markdown_review


def deserialize(file_path: str) -> MarkdownReview:
    with open(file_path, "r") as review_file:
        _, frontmatter, review_content = FM_REGEX.split(review_file.read(), 2)

    review_yaml = yaml.safe_load(frontmatter)

    return MarkdownReview(
        yaml=ReviewYaml(
            work_slug=review_yaml["work_slug"],
            grade=review_yaml["grade"],
            date=review_yaml["date"],
        ),
        review_content=review_content,
    )


def deserialize_all() -> list[MarkdownReview]:
    reviews: list[MarkdownReview] = []
    for review_file_path in glob(os.path.join(FOLDER_NAME, "*.md")):
        reviews.append(deserialize(review_file_path))

    return reviews


def generate_file_path(markdown_review: MarkdownReview) -> str:
    file_path = os.path.join(
        FOLDER_NAME, "{0}.md".format(markdown_review.yaml["work_slug"])
    )

    path_tools.ensure_file_path(file_path)

    return file_path


def serialize(markdown_review: MarkdownReview) -> str:
    file_path = generate_file_path(markdown_review)

    stripped_content = str(markdown_review.review_content or "").strip()

    with open(file_path, "w") as output_file:
        output_file.write("---\n")
        yaml.dump(
            markdown_review.yaml,
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
