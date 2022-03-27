from typing import Sequence

from booklog.reviews import serializer


def all_editions() -> Sequence[str]:
    reviews = serializer.deserialize_all()

    return sorted(set([review.edition for review in reviews]))
