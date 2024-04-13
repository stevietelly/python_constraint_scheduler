from typing import List
from Assets.Functions.Echo import Echo
from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session
from Logic.Structure.Variables import Value, Static
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room

echo = Echo()

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

    def get_static_by_index(self, index: int) -> Static:
        return self.static_variables[index]
   
    def select_unassigned(self) -> Static:
        for index, value in enumerate(self.values):
            if not value.is_filled():
                return self.static_variables[index]
        echo.exit("No More Unassigned Variables")
    
    def all_unassigned(self) -> List[int]:
        unnassigned = []
        for index, value in enumerate(self.values):
            if not value.is_filled():
                unnassigned.append(index)
        return unnassigned

    def check_if_consistent(self, static_variable: Static, value_dict: dict):
        is_group_consistent = self.check_group_consistency(static_variable.group, value_dict["dt"])
        is_room_consistent = self.check_room_consistency(value_dict["r"], value_dict["dt"])
        is_instructor_consistent = True if value_dict["i"] is None else self.check_instructor_consistency(value_dict["i"], value_dict["dt"])
        consistency_problem = "none"
        if not is_group_consistent and not is_room_consistent and not is_instructor_consistent:
            consistency_problem = "all"
        elif not is_group_consistent:
            consistency_problem = "group"
        elif not is_instructor_consistent:
            consistency_problem = "instructor"
        elif not is_room_consistent:
            consistency_problem = "room"
        return all([is_room_consistent, is_group_consistent, is_instructor_consistent]), consistency_problem

    def check_room_consistency(self, room: Room, daytime: DayTime):
        return not any(value.room == room and value.day == daytime.day and value.time == daytime.time for value in self.values)

    def check_instructor_consistency(self, instructor: Instructor, daytime: DayTime):
        return not any(value.instructor == instructor and value.day == daytime.day and value.time == daytime.time for value in self.values)

    def check_group_consistency(self, group: Group, daytime: DayTime):
        for index, static in enumerate(self.static_variables):
            value = self.values[index]
            if static.group == group and value.day and value.time:
                if daytime.time == value.time and daytime.day == value.day:
                    return False
        return True

    def Output(self):
        sessions = []
        identifier =  0
        for index, variable in enumerate(self.static_variables):
            identifier += 1
            values = self.values[index]
            instructor = variable.instructor if variable.instructor is not None else values.instructor
            sessions.append(Session(identifier, variable.group, variable.unit, instructor, DayTime(values.day, values.time), values.room))
        return sessions