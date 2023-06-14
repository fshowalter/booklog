from __future__ import annotations

from booklog.readings.exports import progress, readings  # noqa: WPS235


def export() -> None:  # noqa: WPS213
    readings.export()
    progress.export()
