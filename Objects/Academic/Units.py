from typing import List
from Objects.Internal.Preference.Preference import Rule

class Unit:
    title = str
    sessions = int
    qualified_instructors = list

    def __init__(self,identifier: int, no_of_sessions: int, qualified_instructors: List[int], preferences: Rule):
        self.identifier = identifier
        self.sessions = no_of_sessions
        self.qualified_instructors: List[int] = qualified_instructors

        self.preferences: Rule = preferences
    
    

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Unit: {self.identifier}'

    def __eq__(self, unit) -> bool:
        return self.identifier == unit.identifier

    def __ne__(self, unit) -> bool:
        return self.identifier != unit.identifier

