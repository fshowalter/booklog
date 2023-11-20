import json
import os
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.data.core import api as core_api


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_create_author(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    core_api.create_author(name="Stephen King")

    with open(
        os.path.join(tmp_path / "authors", "stephen-king.json"),
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json


def test_create_create_work(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    author = core_api.create_author("Richard Laymon")

    core_api.create_work(
        title="The Cellar",
        subtitle=None,
        year="1980",
        work_authors=[
            core_api.WorkAuthor(
                author.name,
                author.sort_name,
                author.slug,
                notes=None,
            )
        ],
        kind="Novel",
    )

    with open(
        os.path.join(tmp_path / "works", "the-cellar-by-richard-laymon.json"),
        "r",
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
