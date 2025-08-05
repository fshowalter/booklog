import datetime

from booklog.exports.json_work import JsonWork


class JsonReviewedWork(JsonWork):
    reviewSequence: str
    grade: str
    gradeValue: int
    reviewDate: datetime.date
    yearReviewed: int
