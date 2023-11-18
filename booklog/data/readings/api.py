from __future__ import annotations

from dataclasses import dataclass

from booklog.data.core.api import Work, all_works
from booklog.data.readings import editions, reading, sequence_tools, serializer

TimelineEntry = reading.TimelineEntry

Reading = reading.Reading

all_editions = editions.all_editions

all_readings = serializer.deserialize_all


@dataclass
class ReadingWithWork(Reading):
    work: Work


def all_readings_with_work() -> list[ReadingWithWork]:
    works = all_works()

    return [
        ReadingWithWork(
            sequence=reading.sequence,
            work_slug=reading.work_slug,
            edition=reading.edition,
            timeline=reading.timeline,
            edition_notes=reading.edition_notes,
            work=next(work for work in works if work.slug == reading.work_slug),
        )
        for reading in all_readings()
    ]


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
