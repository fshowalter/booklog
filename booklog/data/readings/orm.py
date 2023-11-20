from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional

from booklog.data.core import api as core_api
from booklog.data.readings import json_readings


@dataclass
class TimelineEntry(object):
    date: datetime.date
    progress: str


@dataclass(kw_only=True)
class Reading(object):
    sequence: int
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: Optional[str] = None
    work: core_api.Work


def create_reading(
    work: core_api.Work,
    timeline: list[TimelineEntry],
    edition: str,
) -> Reading:
    return hydrate_json_reading(
        json_reading=json_readings.create(
            work_slug=work.slug,
            timeline=[
                json_readings.JsonTimelineEntry(
                    date=datetime.date.isoformat(timeline_entry.date),
                    progress=timeline_entry.progress,
                )
                for timeline_entry in timeline
            ],
            edition=edition,
        ),
        work=work,
    )


def hydrate_json_reading(
    json_reading: json_readings.JsonReading,
    work: core_api.Work,
) -> Reading:
    return Reading(
        sequence=json_reading["sequence"],
        timeline=[
            TimelineEntry(
                date=datetime.date.fromisoformat(json_timeline_entry["date"]),
                progress=json_timeline_entry["progress"],
            )
            for json_timeline_entry in json_reading["timeline"]
        ],
        edition=json_reading["edition"],
        edition_notes=json_reading["edition_notes"],
        work=work,
    )
