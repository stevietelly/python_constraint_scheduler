

from typing import Any, Dict, List
from Logic.DateTime.DayTime import DayTime
from Logic.Structure.Session import Session


from Logic.Structure.Variables import Dynamic, Static
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room


class Assignment:
    def __init__(self, static_variables: List[Static]) -> None:
        self.static_variables = static_variables

        self.values = [{"daytime": None, "room": None, "instructor": ""} for _ in self.static_variables]
      

    def get_value(self, static_variable: Static, index: bool=False):
        i = self.static_variables.index(static_variable)
        return self.values[i] if not index else i
    
    def set_value(self, static_variable: Static, value: Dict[str, None | Any]):
        index = self.get_value(static_variable, True)
        self.value[index] = value
    
    def set_daytime(self, static_variable, daytime:DayTime):
        values = self.get_value(static_variable)
        values["daytime"] = daytime

    def get_daytime(self, static_variable):
        values = self.get_value(static_variable)
        return values["daytime"]
    
    def set_instructor(self, static_variable, instructor: Instructor):
        values = self.get_value(static_variable)
        values["instructor"] = instructor

    def get_instructor(self, static_variable):
        values = self.get_value(static_variable)
        return values["instructor"]
    
    def set_room(self, static_variable, room: Room):
        values = self.get_value(static_variable)
        values["room"] = room

    def get_room(self, static_variable):
        values = self.get_value(static_variable)
        return values["room"]

    def is_complete(self)->bool:
        for value in self.values:
            for _, v in value.items():
                if v is None: return False
        return True
    
    def Output (self) -> str:
        sessions = []
        for index, variable in enumerate(self.static_variables):
            values = self.values[index]
            dynamic_variable = Dynamic(None, values["daytime"].time, values["daytime"].day, values["room"])
            sessions.append(Session(variable, dynamic_variable))
           
        return sessions
    
    def __str__(self) -> str:
        return str(self.Output())
    
    def select_unnasigned(self):
        for value in self.values:
            for _, v in value.items():
                if v is None: return self.static_variables[self.values.index(value)]

    def select_all_assigned(self)->List[Static]:
        assigned = []
        
        for index, static_variable in enumerate(self.static_variables):
            if not all([v == None for _, v in self.values[index].items()]): assigned.append(static_variable)
        return assigned
    
    def select_last_assigned(self)->Static:
        return self.select_all_assigned()[-1]
   