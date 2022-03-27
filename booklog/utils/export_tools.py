import json
import os
from collections.abc import Iterable
from typing import TypeVar

from booklog.utils import format_tools
from booklog.utils.logging import logger

DataClassType = TypeVar("DataClassType")
DictType = TypeVar("DictType")

EXPORT_FOLDER_NAME = "export"


def serialize_dicts(dicts: Iterable[DictType], file_name: str) -> None:
    folder_path = os.path.join(EXPORT_FOLDER_NAME)
    os.makedirs(folder_path, exist_ok=True)

    json_file_name = os.path.join(folder_path, "{0}.json".format(file_name))
    with open(json_file_name, "w") as output_file:
        output_file.write(json.dumps(dicts, default=str))

    logger.log(
        "Wrote {} ({}).",
        json_file_name,
        format_tools.pretty_file_size(os.path.getsize(json_file_name)),
    )
