from __future__ import annotations

from booklog.reviews.exports import reviewed_works  # noqa: WPS235


def export() -> None:  # noqa: WPS213
    reviewed_works.export()
