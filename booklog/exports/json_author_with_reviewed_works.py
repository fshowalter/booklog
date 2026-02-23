from booklog.exports.json_author import JsonAuthor


class JsonAuthorWithReviewedWorks(JsonAuthor):
    reviewedWorks: list[str]
