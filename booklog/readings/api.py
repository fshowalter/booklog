from __future__ import annotations

from booklog.readings import editions, reading, serializer
from booklog.readings.exports import api as exports_api
from booklog.utils import sequence_tools

TimelineEntry = reading.TimelineEntry

Reading = reading.Reading

all_editions = editions.all_editions

all_readings = serializer.deserialize_all


def create(
    work_slug: str,
    timeline: list[TimelineEntry],
    edition: str,
) -> Reading:
    sequence = sequence_tools.next_sequence(serializer.deserialize_all())

    new_reading = Reading(
        sequence=sequence,
        work_slug=work_slug,
        timeline=timeline,
        edition=edition,
    )

    serializer.serialize(new_reading)

    return new_reading


def export_data() -> None:
    exports_api.export()
