from booklog.cli import add_author, add_reading, add_work, radio_list
from booklog.exports import api as exports_api
from booklog.utils.logging import logger


@logger.catch
def prompt() -> None:
    options = [
        (add_author.prompt, "<cyan>Add Author</cyan>"),
        (add_work.prompt, "<cyan>Add Work</cyan>"),
        (add_reading.prompt, "<cyan>Add Reading</cyan>"),
        (export, "<cyan>Export Data</cyan>"),
        (None, "Exit"),
    ]

    option_function = radio_list.prompt(
        title="Booklog options:", options=options, rprompt="ESC to exit"
    )
    if option_function:
        option_function()
        prompt()


def export() -> None:
    exports_api.export_data()
