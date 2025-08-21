import datetime

from booklog.exports.json_work import JsonWork


class JsonReviewedWork(JsonWork):
    reviewSequence: str
    grade: str
    gradeValue: int
    gradeSequence: str
    reviewDate: datetime.date
    yearReviewed: int
