from __future__ import annotations

from typing import Optional, Tuple

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.shortcuts import confirm

from booklog.cli import ask
from booklog.data import api as data

Option = Tuple[Optional[str], AnyFormattedText]


def prompt() -> None:
    name = ask_for_name()

    if not name:
        return

    data.create_author(name)


def ask_for_name() -> Optional[str]:
    name = ask.prompt("Name: ")

    if not name:
        return None

    if confirm(name):
        return name

    return ask_for_name()
