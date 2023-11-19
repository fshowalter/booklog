from booklog.cli import add_reading, manage_data, radio_list
from booklog.data import api as data_api
from booklog.logger import logger


@logger.catch
def prompt() -> None:
    options = [
        (manage_data.prompt, "<cyan>Manage Data</cyan>"),
        (add_reading.prompt, "<cyan>Add Reading</cyan>"),
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
    data_api.export_data()
