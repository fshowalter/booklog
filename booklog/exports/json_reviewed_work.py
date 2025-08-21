import datetime

from booklog.exports.json_work import JsonWork


class JsonReviewedWork(JsonWork):
    reviewSequence: int
    grade: str
    gradeValue: int
    gradeSequence: int
    reviewDate: datetime.date
    yearReviewed: int
