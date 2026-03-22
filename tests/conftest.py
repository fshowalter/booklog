from __future__ import annotations

from pathlib import Path

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_exports_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "exports")
    mocker.patch(
        "booklog.exports.exporter.EXPORT_FOLDER_NAME",
        tmp_path / "exports",
    )


@pytest.fixture(autouse=True)
def mock_readings_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "readings")
    mocker.patch("booklog.repository.markdown_readings.FOLDER_NAME", tmp_path / "readings")


@pytest.fixture(autouse=True)
def mock_reviews_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "reviews")
    mocker.patch("booklog.repository.markdown_reviews.FOLDER_NAME", tmp_path / "reviews")


@pytest.fixture(autouse=True)
def mock_titles_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "titles")
    mocker.patch("booklog.repository.json_titles.FOLDER_NAME", tmp_path / "titles")


@pytest.fixture(autouse=True)
def mock_authors_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    Path.mkdir(tmp_path / "authors")
    mocker.patch("booklog.repository.json_authors.FOLDER_NAME", tmp_path / "authors")
