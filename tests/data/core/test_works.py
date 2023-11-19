from booklog.bookdata import works


def test_create_generates_sort_title() -> None:
    expected = "Cellar"

    work_author = works.WorkAuthor("richard-laymon", None)

    work = works.create(
        title="The Cellar",
        subtitle=None,
        year="1980",
        authors=[work_author],
        kind="Novel",
    )

    assert expected == work.sort_title
