from __future__ import annotations

from booklog.exports import (
    authors,
    reading_stats,
    reviewed_works,
    timeline_entries,
    unreviewed_works,
)
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def export_data() -> None:
    repository_data = RepositoryData(
        authors=list(repository_api.authors()),
        works=list(repository_api.works()),
        reviews=list(repository_api.reviews()),
        readings=list(repository_api.readings()),
    )

    authors.export(repository_data)
    reviewed_works.export(repository_data)
    timeline_entries.export(repository_data)
    unreviewed_works.export(repository_data)
    reading_stats.export(repository_data)
