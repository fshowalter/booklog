from __future__ import annotations

from booklog.exports import (
    authors,
    reviewed_works,
    stats,
    timeline_entries,
    unreviewed_works,
)
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def export_data() -> None:
    repository_data = RepositoryData(
        authors=sorted(repository_api.authors(), key=lambda author: author.sort_name),
        works=sorted(repository_api.works(), key=lambda work: work.sort_title),
        reviews=sorted(repository_api.reviews(), key=lambda review: review.work_slug),
        readings=sorted(repository_api.readings(), key=lambda reading: reading.sequence),
    )

    authors.export(repository_data)
    reviewed_works.export(repository_data)
    timeline_entries.export(repository_data)
    unreviewed_works.export(repository_data)
    stats.export(repository_data)
