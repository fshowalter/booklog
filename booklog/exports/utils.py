from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api


def build_review_sequence(
    review: repository_api.Review, repository_data: RepositoryData
) -> str:
    """Build a review sequence string from review and repository data.

    Finds the most recent reading for the reviewed work and combines
    it with the review date to create a unique sequence identifier.

    Raises an error if no reading is found for the reviewed work.
    """
    work = review.work(repository_data.works)
    readings = list(work.readings(repository_data.readings))

    if not readings:
        raise ValueError(f"No readings found for reviewed work: {work.title}")

    most_recent_reading = sorted(
        readings, key=lambda reading: reading.sequence, reverse=True
    )[0]

    return f"{review.date}-{most_recent_reading.sequence}"
