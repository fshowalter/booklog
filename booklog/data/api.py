from __future__ import annotations

from booklog.data.core import api as core_data_api
from booklog.data.exports import api as exports_api
from booklog.data.readings import api as readings_api
from booklog.data.reviews import api as reviews_api

AuthorWithWorks = core_data_api.AuthorWithWorks

CreateWorkAuthor = core_data_api.CreateWorkAuthor

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

create_reading = readings_api.create

all_editions = readings_api.all_editions

WORK_KINDS = core_data_api.WORK_KINDS

create_review = reviews_api.create


def export_data() -> None:
    exports_api.export_data()
