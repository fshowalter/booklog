import os
from datetime import date
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from booklog.data.core import api as core_api
from booklog.data.reviews import api as reviews_api


@pytest.fixture
def created_author() -> core_api.Author:
    return core_api.create_author("Richard Laymon")


@pytest.fixture
def created_work(created_author: core_api.Author) -> core_api.Work:
    return core_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        kind="Novel",
        included_work_slugs=[],
        work_authors=[
            core_api.WorkAuthor(
                name=created_author.name,
                sort_name=created_author.sort_name,
                slug=created_author.slug,
                notes=None,
            )
        ],
    )


def test_can_create_new_review(
    tmp_path: Path, created_work: core_api.Work, snapshot: SnapshotAssertion
) -> None:
    reviews_api.create_or_update(
        work=created_work,
        grade="A+",
        date=date(2016, 3, 10),
    )

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot


def test_can_update_existing_review(
    tmp_path: Path, created_work: core_api.Work, snapshot: SnapshotAssertion
) -> None:
    existing_review = "---\nwork_slug: the-cellar-by-richard-laymon\ngrade: A+\ndate: 2016-03-10\n---\n\nSome review content we want to preserve between updates."  # noqa: 501

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"),
        "w",
    ) as first_output_file:
        first_output_file.write(existing_review)

    reviews_api.create_or_update(
        work=created_work,
        grade="C+",
        date=date(2017, 3, 12),
    )

    with open(
        os.path.join(tmp_path / "reviews", "the-cellar-by-richard-laymon.md"), "r"
    ) as output_file:
        file_content = output_file.read()

    assert file_content == snapshot
