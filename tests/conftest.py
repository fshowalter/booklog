from __future__ import annotations

import os
from pathlib import Path

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_exports_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    os.mkdir(tmp_path / "exports")
    mocker.patch(
        "booklog.data.exports.utils.export_tools.EXPORT_FOLDER_NAME",
        tmp_path / "exports",
    )


@pytest.fixture(autouse=True)
def mock_readings_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    os.mkdir(tmp_path / "readings")
    mocker.patch(
        "booklog.data.readings.json_readings.FOLDER_NAME", tmp_path / "readings"
    )


@pytest.fixture(autouse=True)
def mock_reviews_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    os.mkdir(tmp_path / "reviews")
    mocker.patch(
        "booklog.data.reviews.markdown_reviews.FOLDER_NAME", tmp_path / "reviews"
    )


@pytest.fixture(autouse=True)
def mock_works_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    os.mkdir(tmp_path / "works")
    mocker.patch("booklog.data.core.json_works.FOLDER_NAME", tmp_path / "works")


@pytest.fixture(autouse=True)
def mock_authors_folder_name(mocker: MockerFixture, tmp_path: Path) -> None:
    os.mkdir(tmp_path / "authors")
    mocker.patch("booklog.data.core.json_authors.FOLDER_NAME", tmp_path / "authors")
