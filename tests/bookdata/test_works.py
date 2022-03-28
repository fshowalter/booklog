from booklog.bookdata import works


def test_create_generates_sort_title() -> None:
    expected = "Cellar"

    work_author = works.WorkAuthor("richard-laymon", None)

    work = works.create("The Cellar", None, "1980", [work_author], "Novel")

    assert expected == work.sort_title
