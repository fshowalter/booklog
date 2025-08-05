from booklog.exports.json_author import JsonAuthor
from booklog.exports.json_reviewed_work import JsonReviewedWork


class JsonAuthorWithReviewedWorks(JsonAuthor):
    reviewedWorks: list[JsonReviewedWork]
