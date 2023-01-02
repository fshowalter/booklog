from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Review(object):
    work_slug: str
    date: datetime.date
    grade: Optional[str] = None
    review_content: Optional[str] = None

    @property
    def grade_value(self) -> Optional[float]:
        if not self.grade:
            return None

        value_modifier = 0.33

        grade_map = {
            "A": 5.0,
            "B": 4.0,
            "C": 3.0,
            "D": 2.0,
            "F": 1.0,
        }

        grade_value = grade_map.get(self.grade[0], 3)
        modifier = self.grade[-1]

        if modifier == "+":
            grade_value += value_modifier

        if modifier == "-":
            grade_value -= value_modifier

        return grade_value
