from __future__ import annotations

from booklog.data.readings import orm, queries

TimelineEntry = orm.TimelineEntry

Reading = orm.Reading

all_editions = queries.all_editions

all_readings = queries.all_readings

create_reading = orm.create_reading
