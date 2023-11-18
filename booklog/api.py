from __future__ import annotations

from booklog.bookdata import api as bookdata_api
from booklog.exports import api as exports_api
from booklog.readings import api as readings_api
from booklog.reviews import api as reviews_api

AuthorWithWorks = bookdata_api.AuthorWithWorks

WorkWithAuthors = bookdata_api.WorkWithAuthors

Work = bookdata_api.Work

Author = bookdata_api.Author

WorkAuthor = bookdata_api.WorkAuthor

Review = reviews_api.Review

Reading = readings_api.Reading

TimelineEntry = readings_api.TimelineEntry

create_author = bookdata_api.create_author

search_authors = bookdata_api.search_authors

search_works = bookdata_api.search_works

create_work = bookdata_api.create_work

create_reading = readings_api.create

all_editions = readings_api.all_editions

WORK_KINDS = bookdata_api.WORK_KINDS

create_review = reviews_api.create


def export_data() -> None:
    exports_api.export_data()
