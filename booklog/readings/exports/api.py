from __future__ import annotations

from booklog.readings import serializer
from booklog.readings.exports import readings  # noqa: WPS235


def export() -> None:  # noqa: WPS213
    all_readings = serializer.deserialize_all()
    readings.export(all_readings)
