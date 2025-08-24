import datetime
from typing import Literal

from booklog.exports.json_work import JsonWork


class JsonReviewedWork(JsonWork):
    reviewSequence: int
    grade: str
    gradeValue: int
    gradeSequence: int
    reviewDate: datetime.date
    reviewYear: str
    reviewed: Literal[True]
