from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Callable, DefaultDict, TypeVar

ListType = TypeVar("ListType")


def list_to_dict_by_key(
    iterable: Iterable[ListType], key: Callable[[ListType], str]
) -> dict[str, ListType]:
    items_by_key: DefaultDict[str, ListType] = defaultdict()

    for iterable_item in iterable:
        items_by_key[key(iterable_item)] = iterable_item

    return items_by_key


def group_list_by_key(
    iterable: Iterable[ListType], key: Callable[[ListType], str]
) -> dict[str, list[ListType]]:
    items_by_key = defaultdict(list)

    for iterable_item in iterable:
        items_by_key[key(iterable_item)].append(iterable_item)

    return items_by_key
