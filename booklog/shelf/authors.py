from booklog.bookdata.authors import serialize as serialize_author
from booklog.bookdata.queries import author_for_slug, works_for_author
from booklog.bookdata.works import serialize as serialize_work


def add_author(author_slug: str):
    author = author_for_slug(author_slug=author_slug)
    author.shelf = True
    serialize_author(author)

    works = works_for_author(author_slug=author_slug)
    for work in works:
        work.shelf = True
        serialize_work(work=work)
