from typing import List
from Logic.DateTime.Day import Day

class Week:
    def __init__(self, days: List[Day]):
        "Represents a week"
        self.days: List[Day] = days
        self.start: Day = self.days[0]
        self.end: Day = self.days[-1]
        self.total_no_of_days: int = len(self.days)

    def __str__(self):
        return f'Week:{self.start} To {self.end}'

    def __repr__(self):
        return self.__str__()
