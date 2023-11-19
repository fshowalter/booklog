from __future__ import annotations

from booklog.data.core import api as core_data_api
from booklog.data.exports import api as exports_api
from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api

AuthorWithWorks = core_data_api.AuthorWithWorks

Work = core_data_api.Work

Author = core_data_api.Author

WorkAuthor = core_data_api.WorkAuthor

Review = reviews_api.Review

Reading = readings_api.Reading

TimelineEntry = readings_api.TimelineEntry

create_author = core_data_api.create_author

search_authors = core_data_api.search_authors

search_works = core_data_api.search_works

create_work = core_data_api.create_work

all_editions = readings_api.all_editions

WORK_KINDS = core_data_api.WORK_KINDS

export_data = exports_api.export_data


def create_reading(
    work_slug: str,
    edition: str,
    timeline: list[TimelineEntry],
    grade: str,
) -> None:
    readings_api.create(
        work_slug=work_slug,
        edition=edition,
        timeline=timeline,
    )

    reviews_api.create_or_update(
        work_slug=work_slug,
        date=timeline[-1].date,
        grade=grade,
    )
