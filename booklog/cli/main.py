from booklog import api as booklog_api
from booklog.cli import add_review, manage_data, manage_shelf, radio_list
from booklog.utils.logging import logger


@logger.catch
def prompt() -> None:
    options = [
        (manage_data.prompt, "<cyan>Manage Data</cyan>"),
        (add_review.prompt, "<cyan>Add Review</cyan>"),
        (manage_shelf.prompt, "<cyan>Manage Shelf</cyan>"),
        (export, "<cyan>Export Data</cyan>"),
        (None, "Exit"),
    ]

    option_function = radio_list.prompt(
        title="Booklog options:",
        options=options,
    )
    if option_function:
        option_function()
        prompt()


def export() -> None:
    booklog_api.export_data()
