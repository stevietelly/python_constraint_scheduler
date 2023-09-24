from Objects.User.Preference.Preference import Rule
from typing import List

class Unit:
    title = str
    sessions = int
    qualified_instructors = list

    def __init__(self,identifier: int, title: str, no_of_sessions: int, qualified_instructors: List[int], preferences: Rule):
        self.identifier = identifier
        self.title = title
        self.sessions = no_of_sessions
        self.qualified_instructors = qualified_instructors

        self.preferences: Rule = preferences
    
    

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Unit: {self.title}'

    def __eq__(self, unit) -> bool:
        return (self.title == unit.title) and (self.sessions == unit.sessions)

    def __ne__(self, unit) -> bool:
        return (self.title != unit.title) or (self.sessions != unit.sessions)

