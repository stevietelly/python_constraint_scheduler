from typing import List

from Objects.Persons.Students import Group


class Programme:
    title = str
    school = str
    department = str
 

    def __init__(self, identifier: int,  title: str, levels: int=None):
        self.title = title
        self.identifier = identifier
        self.levels = levels
        self.units: List[List[int]]
        self.groups: List[Group] = list()


    def __repr__(self):
        return f"Programme: {self.title}"

    def __str__(self):
        return f"Programme: {self.title}"
