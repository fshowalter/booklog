import datetime

from booklog.exports.json_work import JsonWork


class JsonMaybeReviewedWork(JsonWork):
    grade: str | None
    gradeValue: int | None
    reviewDate: datetime.date | None
    reviewYear: str | None
    reviewed: bool
