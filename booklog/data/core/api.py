from __future__ import annotations

from booklog.data.core import json_works, orm, queries

Work = orm.Work

Author = orm.Author

AuthorWithWorks = orm.AuthorWithWorks

WorkAuthor = orm.WorkAuthor

WORK_KINDS = json_works.KINDS

search_authors = queries.search_authors

search_works = queries.search_works

create_work = orm.create_work

create_author = orm.create_author

all_authors_and_works = queries.all_authors_and_works
