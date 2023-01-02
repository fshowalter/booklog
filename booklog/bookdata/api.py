from __future__ import annotations

from booklog.bookdata import authors, queries, works
from booklog.bookdata.exports import api as exports_api

all_authors = authors.deserialize_all

all_works = works.deserialize_all

create_author = authors.create

create_work = works.create

WORK_KINDS = works.KINDS

WorkAuthor = works.WorkAuthor

Work = works.Work

Author = authors.Author

search_authors = queries.search_authors

search_works = queries.search_works

AuthorWithWorks = queries.AuthorWithWorks

WorkWithAuthors = queries.WorkWithAuthors


def export_data() -> None:
    exports_api.export()
