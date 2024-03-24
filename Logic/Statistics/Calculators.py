

from typing import List
from Logic.Compliance.Negative import Clash, GroupClash, InstructorClash, RoomClash
from Logic.Compliance.Positive import FreeGroupPeriod, FreeInstructorPeriod, FreePeriod, FreeRoomPeriod

from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class Calculator:
    def __init__(self, object_, daytimes: List[DayTime], object_clash, object_free_period) -> None:
        self.object =  object_
        self.sessions: List[Session] = []
        self.type_ = None
        
        self.daytimes = daytimes
        self.session_timelines = {}

        self.object_clash: Clash = object_clash
        self.clashes: List[Clash] = list()
        self.free_period : FreePeriod = object_free_period
        self.free_periods: List[FreePeriod] =  list()
        
   
    def AddSessions(self, *session: Session):
        self.sessions.extend(session)
    
    def Analyse(self):
        self.Divide()
        self.ClashCheck()

    def Divide(self):

        for session in self.sessions:
            if session.daytime in self.session_timelines.keys(): self.session_timelines[session.daytime].append(session)
            else: self.session_timelines[session.daytime] = [session]
          
    def ClashCheck(self):
        for daytime, sessions in self.session_timelines.items():
            total = len(sessions)
            if total > 1:
                object_clash: Clash = self.object_clash(self.object, daytime) 
                object_clash.AddSessionIdentifiers(*[s.identifier for s in sessions])
                self.clashes.append(object_clash)
            
            elif total <= 1: 
                
                self.free_period(self.object, daytime)

class GroupCalculator(Calculator):
    def __init__(self, group: Group, daytimes) -> None:
        super().__init__(group, daytimes, GroupClash, FreeGroupPeriod)
        self.type_ = "groups"

class RoomCalculator(Calculator):
    def __init__(self, room: Room, daytimes) -> None:
        super().__init__(room, daytimes, RoomClash, FreeRoomPeriod)
        self.type_ = "rooms"

class InstructorCalculator(Calculator):
    def __init__(self, room: Instructor, daytimes) -> None:
        super().__init__(room, daytimes, InstructorClash, FreeInstructorPeriod)
        self.type_ = "instructors"
    