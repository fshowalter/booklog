from __future__ import annotations

import datetime
import json
import os
import re
from dataclasses import asdict, dataclass
from glob import glob
from typing import Any, Optional, Sequence, TypedDict, cast

import yaml
from slugify import slugify

from booklog.utils import path_tools
from booklog.utils.logging import logger


@dataclass
class TimelineEntry(object):
    date: datetime.date
    progress: str


@dataclass
class OldReview(object):
    sequence: int
    slug: str
    edition: str
    timeline: list[TimelineEntry]
    grade: Optional[str] = None
    edition_notes: Optional[str] = None
    review_content: Optional[str] = None


@dataclass
class NewReview(object):
    work_slug: str
    date: datetime.date
    grade: Optional[str] = None
    review_content: Optional[str] = None


@dataclass
class Reading(object):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: Optional[str] = None


FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


class TimelineYaml(TypedDict):
    date: datetime.date
    progress: str


class OldReviewYaml(TypedDict):
    sequence: int
    slug: str
    grade: Optional[str]
    edition: str
    timeline: list[TimelineYaml]
    edition_notes: Optional[str]


class NewReviewYaml(TypedDict):
    work_slug: str
    grade: Optional[str]
    date: datetime.date


def deserialize_timeline(review_yaml: OldReviewYaml) -> list[TimelineEntry]:
    timeline = []

    for timeline_entry in review_yaml["timeline"]:
        timeline.append(
            TimelineEntry(
                date=timeline_entry["date"], progress=timeline_entry["progress"]
            )
        )

    return timeline


def deserialize(file_path: str) -> OldReview:
    with open(file_path, "r") as review_file:
        _, frontmatter, review_content = FM_REGEX.split(review_file.read(), 2)

    review_yaml = cast(OldReviewYaml, yaml.safe_load(frontmatter))

    timeline = deserialize_timeline(review_yaml=review_yaml)

    return OldReview(
        grade=review_yaml["grade"],
        slug=review_yaml["slug"],
        sequence=review_yaml["sequence"],
        edition=review_yaml["edition"],
        edition_notes=review_yaml["edition_notes"],
        timeline=timeline,
        review_content=review_content,
    )


def deserialize_all() -> Sequence[OldReview]:
    reviews: list[OldReview] = []
    for review_file_path in glob(os.path.join("reviews-back", "*.md")):
        reviews.append(deserialize(review_file_path))

    reviews.sort(key=lambda review: review.sequence)

    return reviews


def generate_file_path(review: NewReview) -> str:
    file_name = slugify(
        "{0}".format(review.work_slug),
    )

    file_path = os.path.join("reviews", "{0}.md".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def generate_reading_file_path(reading: Reading) -> str:
    file_name = slugify(
        "{0:04d} {1}".format(reading.sequence, reading.work_slug),
    )

    file_path = os.path.join("readings", "{0}.json".format(file_name))

    path_tools.ensure_file_path(file_path)

    return file_path


def generate_yaml(review: NewReview) -> NewReviewYaml:
    return NewReviewYaml(
        work_slug=review.work_slug,
        grade=review.grade,
        date=review.date,
    )


def serialize(review: NewReview) -> str:
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


def serialize_reading(reading: Reading) -> str:
    file_path = generate_reading_file_path(reading)

    with open(file_path, "w") as output_file:
        json.dump(asdict(reading), output_file, indent=4, default=str)

    logger.log("Wrote {}", file_path)

    return file_path


def refactor() -> None:
    old_reviews = deserialize_all()

    for old_review in old_reviews:
        new_review = NewReview(
            work_slug=old_review.slug,
            grade=old_review.grade,
            review_content=old_review.review_content,
            date=old_review.timeline[-1].date,
        )

        new_reading = Reading(
            sequence=old_review.sequence,
            work_slug=old_review.slug,
            edition=old_review.edition,
            edition_notes=old_review.edition_notes,
            timeline=old_review.timeline,
        )

        serialize_reading(new_reading)
        serialize(new_review)


if __name__ == "__main__":
    refactor()
