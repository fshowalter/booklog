from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Callable, TypeVar

ListType = TypeVar("ListType")
KeyType = TypeVar("KeyType")


def group_list_by_key(
    iterable: Iterable[ListType], key: Callable[[ListType], KeyType]
) -> dict[KeyType, list[ListType]]:
    items_by_key = defaultdict(list)

    for iterable_item in iterable:
        items_by_key[key(iterable_item)].append(iterable_item)

    return items_by_key
