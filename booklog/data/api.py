from __future__ import annotations

from booklog.data.core import api as core_api
from booklog.data.exports import api as exports_api
from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api

AuthorWithWorks = core_api.AuthorWithWorks

Work = core_api.Work

Author = core_api.Author

WorkAuthor = core_api.WorkAuthor

Review = reviews_api.Review

Reading = readings_api.Reading

TimelineEntry = readings_api.TimelineEntry

create_author = core_api.create_author

search_authors = core_api.search_authors

search_works = core_api.search_works

create_work = core_api.create_work

all_editions = readings_api.all_editions

WORK_KINDS = core_api.WORK_KINDS

export_data = exports_api.export_data


def create_reading(
    work: core_api.Work,
    edition: str,
    timeline: list[TimelineEntry],
    grade: str,
) -> None:
    readings_api.create_reading(
        work=work,
        edition=edition,
        timeline=timeline,
    )

    reviews_api.create_or_update(
        work=work,
        date=timeline[-1].date,
        grade=grade,
    )
