

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
      

    def get_value(self, static_variable: Static, index: bool=False):
        i = self.static_variables.index(static_variable)
        return self.values[i] if not index else i
    
    def set_value(self, static_variable: Static, value: Dict[str, None | Any]):
        i = self.static_variables.index(static_variable)
        
        self.values[i] = value
    
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
        for i in range(len(self.values)):
            for j in range(i + 1, len(self.values)):
                if self.values[i] == self.values[j]:
                    return True
        return False
    def check_if_consistent(self, value):
        self.values.append(value)
        check  = self.is_consistent()
        self.values.pop()
        return check

    def Output (self) -> str:
        sessions = []
        for index, variable in enumerate(self.static_variables):
            values = self.values[index]
            dynamic_variable = Dynamic(values["daytime"].time, values["daytime"].day, values["room"])
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
   