from booklog.cli import add_review, manage_data, radio_list
from booklog.data import api as data_api
from booklog.data.core import json_works
from booklog.logger import logger


@logger.catch
def prompt() -> None:
    options = [
        (manage_data.prompt, "<cyan>Manage Data</cyan>"),
        (add_review.prompt, "<cyan>Add Review</cyan>"),
        (export, "<cyan>Export Data</cyan>"),
        (migrate, "<cyan>Migrate Data</cyan>"),
        (None, "Exit"),
    ]

    option_function = radio_list.prompt(
        title="Booklog options:",
        options=options,
    )
    if option_function:
        option_function()
        prompt()


def migrate() -> None:
    for json_work in json_works.deserialize_all():
        json_works.serialize(json_work)


def export() -> None:
    data_api.export_data()
