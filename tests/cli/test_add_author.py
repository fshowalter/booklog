from __future__ import annotations

import json
from pathlib import Path

from booklog.cli import add_author
from tests.cli.conftest import MockInput
from tests.cli.keys import Enter, Escape
from tests.cli.prompt_utils import enter_text


def test_creates_author(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input(enter_text("Stephen King", confirm="y"))

    add_author.prompt()

    data = json.loads((tmp_path / "authors" / "stephen-king.json").read_text())
    assert data["name"] == "Stephen King"


def test_can_cancel_out(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input([Escape])

    add_author.prompt()

    assert list((tmp_path / "authors").glob("*.json")) == []


def test_does_not_add_blank_author(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input([Enter])

    add_author.prompt()

    assert list((tmp_path / "authors").glob("*.json")) == []


def test_can_correct_input(mock_input: MockInput, tmp_path: Path) -> None:
    mock_input(
        [
            *enter_text("Steven Kang", confirm="n"),
            *enter_text("Stephen King", confirm="y"),
        ]
    )

    add_author.prompt()

    data = json.loads((tmp_path / "authors" / "stephen-king.json").read_text())
    assert data["name"] == "Stephen King"
