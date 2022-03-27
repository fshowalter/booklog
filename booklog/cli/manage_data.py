from booklog.cli import add_author, add_work, radio_list


def prompt() -> None:
    options = [
        (None, "Go back"),
        (add_author.prompt, "<cyan>Add Author</cyan>"),
        (add_work.prompt, "<cyan>Add Work</cyan>"),
    ]

    option_function = radio_list.prompt(
        title="Manage Data:",
        options=options,
    )

    if option_function:
        option_function()
        prompt()
