from typing import Sequence

from booklog.readings import serializer


def all_editions() -> Sequence[str]:
    readings = serializer.deserialize_all()

    return sorted(set([reading.edition for reading in readings]))
