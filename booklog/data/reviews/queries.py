from booklog.data.core import api as core_api
from booklog.data.reviews import markdown_reviews, orm


def all_reviews(
    all_works: list[core_api.Work],
) -> list[orm.Review]:
    return [
        orm.hydrate_markdown_review(
            markdown_review=markdown_review,
            work=next(
                work
                for work in all_works
                if work.slug == markdown_review.yaml["work_slug"]
            ),
        )
        for markdown_review in markdown_reviews.deserialize_all()
    ]
