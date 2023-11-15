import json
import os
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from booklog.bookdata import authors, works
from booklog.exports import readings
from booklog.readings import serializer as reading_serializer
from booklog.readings.reading import Reading


@pytest.fixture(autouse=True)
def init_data() -> None:
    author = authors.create("Stephen King")
    work = works.create(
        title="On Writing",
        subtitle="A Memoir of the Craft",
        year="2000",
        authors=[works.WorkAuthor(slug=author.slug, notes=None)],
        kind="Nonfiction",
    )
    reading = Reading(sequence=1, work_slug=work.slug, edition="Kindle", timeline=[])
    reading_serializer.serialize(reading)


@pytest.fixture
def snapshot_json(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)


def test_exports_readings(tmp_path: Path, snapshot_json: SnapshotAssertion) -> None:
    readings.export(
        authors=authors.deserialize_all(),
        readings=reading_serializer.deserialize_all(),
        works=works.deserialize_all(),
    )

    with open(
        os.path.join(tmp_path / "exports", "new_readings.json"), "r"
    ) as output_file:
        file_content = json.load(output_file)

    assert file_content == snapshot_json
