from datetime import date
from typing import TypedDict

from booklog.reviews import serializer
from booklog.utils import export_tools
from booklog.utils.logging import logger

JsonReview = TypedDict(
    "JsonReview",
    {
        "gradeValue": int,
        "workSlug": str,
        "grade": str,
        "reviewDate": date,
        "reviewYear": int,
    },
)


def export() -> None:
    logger.log("==== Begin exporting {}...", "readings")

    json_reviews = [
        JsonReview(
            grade=review.grade,
            workSlug=review.work_slug,
            gradeValue=review.grade_value,
            reviewDate=review.date,
            reviewYear=review.date.year,
        )
        for review in serializer.deserialize_all()
    ]

    export_tools.serialize_dicts(json_reviews, "reviewed_works")
