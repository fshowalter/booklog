from dataclasses import dataclass

from booklog.repository import api as repository_api


@dataclass
class RepositoryData:
    authors: list[repository_api.Author]
    authors_with_reviews: set[str]
    titles: list[repository_api.Title]
    readings: list[repository_api.Reading]
    reviews: list[repository_api.Review]
