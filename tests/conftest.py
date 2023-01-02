from __future__ import annotations

import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_exports_folder_name(mocker: MockerFixture, tmp_path: str) -> None:
    mocker.patch("booklog.utils.export_tools.EXPORT_FOLDER_NAME", tmp_path)


@pytest.fixture(autouse=True)
def mock_readings_folder_name(mocker: MockerFixture, tmp_path: str) -> None:
    mocker.patch("booklog.readings.serializer.FOLDER_NAME", tmp_path)


@pytest.fixture(autouse=True)
def mock_reviews_folder_name(mocker: MockerFixture, tmp_path: str) -> None:
    mocker.patch("booklog.reviews.serializer.FOLDER_NAME", tmp_path)


@pytest.fixture(autouse=True)
def mock_works_folder_name(mocker: MockerFixture, tmp_path: str) -> None:
    mocker.patch("booklog.bookdata.works.FOLDER_NAME", tmp_path)


@pytest.fixture(autouse=True)
def mock_authors_folder_name(mocker: MockerFixture, tmp_path: str) -> None:
    mocker.patch("booklog.bookdata.authors.FOLDER_NAME", tmp_path)
