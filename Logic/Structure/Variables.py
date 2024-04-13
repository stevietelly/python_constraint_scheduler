from typing import List
from Assets.Functions.Utilities import return_list_of_daytimes
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class Static:
    """
    An Unchanging Variable
    contains
    1. Unit
    2. Group
    3. Instructor
    """
    def __init__(self, identifier: int, unit, group, instructor=None) -> None:
        self.identifier =  identifier
        self.group: Group = group
        self.unit: Unit = unit
        self.instructor: Instructor = instructor
    def __repr__(self):
        return f'StaticVariable: {self.identifier} with {self.group} taking {self.unit}'
    def __str__(self):
        return f'StaticVariable: {self.identifier} with {self.group} taking {self.unit}'

    def __eq__(self, static):
        if not isinstance(static, Static): return False
        return (self.group.identifier == static.group.identifier) and (self.unit.identifier == static.unit.identifier) and (self.identifier == static.identifier)

    def __ne__(self, static):
        if not isinstance(static, Static): return False
        return (self.group.identifier != static.group.identifier) and (self.unit.identifier != static.unit.identifier) and (self.identifier != static.identifier)


class Dynamic:
    """
    A Changing Variable

    """
    def __init__(self, times: List[Time], days: List[Day], rooms: List[Room], instructors: List[Instructor]) -> None:
        self.times: List[Time] = times
        self.days: List[Day] = days
        self.daytimes: List[DayTime] = return_list_of_daytimes(self.days, self.times)
        self.rooms: List[Room] = rooms
        self.instructors: List[Instructor] = instructors

    def __str__(self):
        return f'DynamicVariable with {len(self.daytimes)} daytimes and {len(self.rooms)} rooms'
    
    def __len__(self):
        return len(self.daytimes) + len(self.rooms) + len(self.instructors)


class Value:
    """
    Value for an Assignmesnt
    """
    def __init__(self) -> None:
        self.day = None
        self.time =  None
        self.room: Room = None
        self.instructor: Instructor = None
        
    
    def is_filled(self)->bool:
        
        return all([self.day is not None, self.time is not None, self.room is not None, self.instructor is not None])