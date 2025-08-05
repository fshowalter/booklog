from booklog.exports.json_author import JsonAuthor
from booklog.repository import api as repository_api


class JsonWorkAuthor(JsonAuthor):
    notes: str | None


def build_json_work_author(
    work_author: repository_api.WorkAuthor, all_authors: list[repository_api.Author]
) -> JsonWorkAuthor:
    author = work_author.author(all_authors)

    return JsonWorkAuthor(
        slug=author.slug,
        notes=work_author.notes,
        name=author.name,
        sortName=author.sort_name,
    )
