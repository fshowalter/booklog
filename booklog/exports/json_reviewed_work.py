import datetime
from typing import Literal

from booklog.exports.json_work import JsonWork


class JsonReviewedWork(JsonWork):
    reviewSequence: str
    grade: str
    gradeValue: int
    reviewDate: datetime.date
    reviewYear: str
    reviewed: Literal[True]
