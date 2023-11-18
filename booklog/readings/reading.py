from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimelineEntry(object):
    date: datetime.date
    progress: str


@dataclass(kw_only=True)
class Reading(object):
    sequence: int
    work_slug: str
    edition: str
    timeline: list[TimelineEntry]
    edition_notes: Optional[str] = None
