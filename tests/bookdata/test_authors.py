from booklog.bookdata import authors


def test_create_generates_sort_name() -> None:
    expected = "King, Stephen"

    author = authors.create("Stephen King")

    assert expected == author.sort_name
