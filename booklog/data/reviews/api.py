from __future__ import annotations

from booklog.data.reviews import orm, queries

Review = orm.Review

all_reviews = queries.all_reviews

create_or_update = orm.create_or_update
