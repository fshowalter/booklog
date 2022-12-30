from booklog.cli import add_author_to_shelf, radio_list


def prompt() -> None:
    options = [
        (None, "Go back"),
        (add_author_to_shelf.prompt, "<cyan>Add Author</cyan>"),
    ]

    option_function = radio_list.prompt(
        title="Manage Watchlist:",
        options=options,
    )

    if option_function:
        option_function()
        prompt()
