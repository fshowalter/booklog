from __future__ import annotations

from booklog.bookdata import api as bookdata_api
from booklog.readings import api as readings_api
from booklog.shelf import api as shelf_api

AuthorWithWorks = bookdata_api.AuthorWithWorks

WorkWithAuthors = bookdata_api.WorkWithAuthors

Work = bookdata_api.Work

TimelineEntry = readings_api.TimelineEntry

create_author = bookdata_api.create_author

search_authors = bookdata_api.search_authors

search_works = bookdata_api.search_works

create_work = bookdata_api.create_work

create_reading = readings_api.create

all_editions = readings_api.all_editions

WORK_KINDS = bookdata_api.WORK_KINDS

add_author_to_shelf = shelf_api.add_author


def export_data() -> None:
    readings_api.export_data()
    bookdata_api.export_data()
