from typing import Any, Dict, List
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Logic.Structure.Session import Session
from Logic.Structure.Variables import Value, Static
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room


class Assignment:
    """
    Assignment
    ___
    """
    def __init__(self, static_variables: List[Static], value: Value) -> None:
        self.static_variables: List[Static] = static_variables
        self.values: List[Value] = [value for _ in self.static_variables]
        self.last_assigned: Static = None
        self.instructors_static = self.static_variables[0].instructor is None
    
    def set_value(self,static_variable: Static, value: Value):
        for index, variable in enumerate(self.static_variables):
            if variable == static_variable:
                self.last_assigned = index
                self.values[index] = value


    def is_complete(self)->bool:
        # Check if all the values are filled
        return all(value.is_filled() for value in self.values)
   
    def select_unassigned(self):
        
        for index, value in enumerate(self.values):
            if not value.is_filled():
                return self.static_variables[index]
        print("No More Unassigned Variables")
    
    def check_if_consistent(self, value_dict: dict):
        is_room_consistent = self.check_room_consistency(value_dict["r"], value_dict["d"], value_dict["t"])
        is_instructor_consistent = True if value_dict["i"] is None else self.check_instructor_consistency(value_dict["i"], value_dict["d"], value_dict["t"])
        consistency_problem = "both" if not is_room_consistent and not is_instructor_consistent else "none"
        if not is_instructor_consistent: consistency_problem = "instructor"
        elif not is_room_consistent: consistency_problem = "room"
        return all([is_room_consistent, is_instructor_consistent]), consistency_problem


    def check_room_consistency(self, room: Room, day: Day, time: Time):
        return not any(value.room == room and value.day == day and value.time == time for value in self.values)
        
    
    def check_instructor_consistency(self, instructor: Instructor, day: Day, time: Time):
        return not any(value.instructor == instructor and value.day == day and value.time == time for value in self.values)
        
    def Output(self):
        sessions = []
        identifier =  0
        for index, variable in enumerate(self.static_variables):
            identifier += 1
            values = self.values[index]
            instructor = variable.instructor if variable.instructor is not None else values.instructor
            sessions.append(Session(identifier, variable.group, variable.unit, instructor, DayTime(values.day, values.time), values.room))
        return sessions