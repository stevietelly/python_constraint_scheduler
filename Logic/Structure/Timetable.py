from typing import List
from Logic.Structure.Configuration import Configuration

from Logic.Structure.Session import Session


class Timetable:
    def __init__(self,sessions: List[Session]) -> None:
       
        self.sessions =  sessions
        return self.Output()
    
    def Output(self):
        sessions = []
        for session in self.sessions:
            sessions.append(session.serialize())
        return sessions 
        
