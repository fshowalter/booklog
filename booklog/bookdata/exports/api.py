from __future__ import annotations

from booklog.bookdata.exports import authors, works


def export() -> None:  # noqa: WPS213
    authors.export()
    works.export()
