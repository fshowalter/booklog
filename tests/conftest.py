from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

_FM_REGEX = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def read_yaml_frontmatter(file_path: Path) -> dict:  # type: ignore[type-arg]
    _, frontmatter, _ = _FM_REGEX.split(file_path.read_text(), 2)
    return yaml.safe_load(frontmatter)  # type: ignore[no-any-return]


@pytest.fixture(autouse=True)
def mock_exports_folder_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "exports")
    monkeypatch.setattr(
        "booklog.exports.exporter.EXPORT_FOLDER_NAME",
        tmp_path / "exports",
    )


@pytest.fixture(autouse=True)
def mock_readings_folder_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "readings")
    monkeypatch.setattr("booklog.repository.markdown_readings.FOLDER_NAME", tmp_path / "readings")


@pytest.fixture(autouse=True)
def mock_reviews_folder_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "reviews")
    monkeypatch.setattr("booklog.repository.markdown_reviews.FOLDER_NAME", tmp_path / "reviews")


@pytest.fixture(autouse=True)
def mock_titles_folder_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "titles")
    monkeypatch.setattr("booklog.repository.json_titles.FOLDER_NAME", tmp_path / "titles")


@pytest.fixture(autouse=True)
def mock_authors_folder_name(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "authors")
    monkeypatch.setattr("booklog.repository.json_authors.FOLDER_NAME", tmp_path / "authors")
