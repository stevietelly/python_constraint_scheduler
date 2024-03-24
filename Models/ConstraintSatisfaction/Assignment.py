

from typing import Any, Dict, List
from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session


from Logic.Structure.Variables import Dynamic, Static
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room


class Assignment:
    def __init__(self, static_variables: List[Static], values: dict) -> None:
        self.static_variables = static_variables

        self.values = [values for _ in self.static_variables]
        self.last_assigned: Static = None

        self.instructors_static = self.static_variables[0].instructor is None

    def get_value(self, static_variable: Static, index: bool=False):
        i = self.static_variables.index(static_variable)
        return self.values[i] if not index else i
    
    def set_value(self, static_variable: Static, value: Dict[str, None | Any]):
        i = self.static_variables.index(static_variable)
        
        self.values[i] = value
        self.last_assigned = static_variable
    
    def set_specific_value(self, static_variable, value, type):
        values = self.get_value(static_variable)
        values[type] = value

    def get_specific_value(self, static_variable, type):
        values = self.get_value(static_variable)
        return values[type]
    
    def is_complete(self)->bool:
        for value in self.values:
        
            for _, v in value.items():
     
                if v is None: return False
        return True
    
    def is_consistent(self)->bool:
        last_variable = self.select_last_assigned()
        value = self.get_value(last_variable)
        if self.values.count(value) == 1: return True
        return False
    
    def check_if_consistent(self, variable, value):
        if None in value.values(): return False

        if self.instructors_static:
            for vls in self.values:
                if None in vls.values(): break
                room_clashes = [v["room"] == vls["room"] and v["daytime"] == vls["daytime"] for v in self.values]
                instructor_clashes = [v["instructor"] == vls["instructor"] and v["daytime"] == vls["daytime"] for v in self.values]
                if any(instructor_clashes) or room_clashes: return False
        return not value in self.values

    def Output (self) -> str:
        
        sessions = []
        identifier =  0
        for index, variable in enumerate(self.static_variables):
            identifier += 1
            values = self.values[index]
            instructor = values["instructor"] if self.instructors_static else variable.instructor

           
            sessions.append(Session(identifier, variable.group, variable.unit, instructor, values["daytime"], values["room"]))
           
        return sessions
    
    def __str__(self) -> str:
        return str(self.Output())
    
    def check_if_assigned(self, variable):
        values: dict = self.get_value(variable)
        for _, v in values.items():
            if v is None: return False
        return True 
    
    def select_unnasigned(self):
        for index, value in enumerate(self.values):
            for _, v in value.items():
                if v is None: return self.static_variables[index]

    def select_all_assigned(self)->List[Static]:
        assigned = []
        
        for index, static_variable in enumerate(self.static_variables):
            if not all([v == None for _, v in self.values[index].items()]): assigned.append(static_variable)
        return assigned
    
    def select_last_assigned(self)->Static:
        return self.last_assigned
   