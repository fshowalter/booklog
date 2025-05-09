from __future__ import annotations

import datetime
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict, cast

import yaml

from booklog.utils import path_tools
from booklog.utils.logging import logger

FOLDER_NAME = "reviews"

FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


@dataclass(kw_only=True)
class MarkdownReview:
    yaml: ReviewYaml
    review_content: str | None = None


class ReviewYaml(TypedDict):
    work_slug: str
    grade: str
    date: datetime.date


def create_or_update(
    work_slug: str,
    grade: str,
    date: datetime.date,
) -> MarkdownReview:
    markdown_review = next(
        (
            markdown_review
            for markdown_review in read_all()
            if markdown_review.yaml["work_slug"] == work_slug
        ),
        None,
    )

    if markdown_review:
        markdown_review.yaml["date"] = date
        markdown_review.yaml["grade"] = grade
    else:
        markdown_review = MarkdownReview(
            yaml=ReviewYaml(
                work_slug=work_slug,
                grade=grade,
                date=date,
            )
        )

    serialize(markdown_review)

    return markdown_review


def read_all() -> Iterable[MarkdownReview]:
    for file_path in Path(FOLDER_NAME).glob("*.md"):
        with Path.open(file_path) as review_file:
            _, frontmatter, review_content = FM_REGEX.split(review_file.read(), 2)
            yield MarkdownReview(
                yaml=cast(ReviewYaml, yaml.safe_load(frontmatter)),
                review_content=review_content,
            )


def generate_file_path(markdown_review: MarkdownReview) -> Path:
    file_path = Path(FOLDER_NAME) / f"{markdown_review.yaml["work_slug"]}.md"

    path_tools.ensure_file_path(file_path)

    return file_path


def serialize(markdown_review: MarkdownReview) -> Path:
    file_path = generate_file_path(markdown_review)

    stripped_content = str(markdown_review.review_content or "").strip()

    with Path.open(file_path, "w") as output_file:
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
