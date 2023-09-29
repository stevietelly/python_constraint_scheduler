from typing import List
from Logic.Structure.Configuration import Configuration

from Logic.Structure.Session import Session


class Timetable:
    def __init__(self,sessions: List[Session]) -> None:
       
        self.sessions =  sessions
        self.EvaluateTimetable()
    
    def EvaluateTimetable(self):
        for session in self.sessions:
            preferences = []
            preferences.append(session.static_variable.group.preferences)
            preferences.append(session.static_variable.instructor.preferences)
            preferences.append(session.static_variable.unit.preferences)
        
    
    def Output(self):
        sessions = []
        for session in self.sessions:
            sessions.append(session.serialize())
        return sessions 
        
