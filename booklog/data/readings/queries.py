from typing import Sequence

from booklog.data.core import api as core_api
from booklog.data.readings import json_readings, orm


def all_editions() -> Sequence[str]:
    readings = json_readings.deserialize_all()

    return sorted(set([reading["edition"] for reading in readings]))


def all_readings(
    all_works: list[core_api.Work],
) -> list[orm.Reading]:
    return [
        orm.hydrate_json_reading(
            json_reading=json_reading,
            work=next(
                work for work in all_works if work.slug == json_reading["work_slug"]
            ),
        )
        for json_reading in json_readings.deserialize_all()
    ]
