from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable
from typing import TypeVar

_ListType = TypeVar("_ListType")


def list_to_dict_by_key(
    iterable: Iterable[_ListType], key: Callable[[_ListType], str]
) -> dict[str, _ListType]:
    items_by_key: defaultdict[str, _ListType] = defaultdict()

    for iterable_item in iterable:
        items_by_key[key(iterable_item)] = iterable_item

    return items_by_key


def group_list_by_key(
    iterable: Iterable[_ListType], key: Callable[[_ListType], str]
) -> dict[str, list[_ListType]]:
    items_by_key = defaultdict(list)

    for iterable_item in iterable:
        items_by_key[key(iterable_item)].append(iterable_item)

    return items_by_key
