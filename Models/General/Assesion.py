from typing import List
from Logic.Structure.Session import Session
from Logic.Structure.Variables import Static


class Assesion:
    def __init__(self, static_variables: List[Static]) -> List[Session]:
        self.static_variables = static_variables
        self.sessions = list()
        self.Fix()
        return self.sessions
    
    def Fix(self):
        for static_variable in self.static_variables:
            self.sessions.append(Session(static_variable))