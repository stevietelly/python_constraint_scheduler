from typing import List, Tuple

from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Logic.Structure.Variables import Dynamic, Static
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room


class Domain:
    """
    The Domain
    a holder for the variables and values
    """
    def __init__(self, static_variables: List[Static], dynamic_variables: List[Dynamic]) -> None:
        self.variables = static_variables
        self.values = dynamic_variables
        self.taken_values = {}
    
    def set_dynamic_variable(self, static_variable: Static, dynamic_variable: Dynamic) -> None:
        index = self.variables.index(static_variable)
        self.values[index] = dynamic_variable
    
    def get_values(self, variable: Static):
        index= self.variables.index(variable)
        return self.values[index]


    def get_next_value(self, variable: Static, index: dict)->Tuple[dict, str]:
        variable_index = self.variables.index(variable)
        dynamic_variable = self.values[variable_index]
        return self.parse_dynamic_variable(dynamic_variable, index)
    
    def parse_dynamic_variable(self, dynamic_variable: Dynamic, index: dict)->Tuple[dict, str]:
        restart = None
        instructor, i_restart = self.next_instructor(dynamic_variable.instructors, index["i"])
        day, d_restart = self.next_day(dynamic_variable.days, index["d"])
        time, t_restart = self.next_time(dynamic_variable.times, index["t"])
        room, r_restart = self.next_room(dynamic_variable.rooms, index["r"])

        match [r_restart, d_restart, t_restart, i_restart]:
            case [True, False, False, False]:
                restart = "room"
            case [False, True, False, False]:
                restart = "day"
            case [False, False, True, False]:
                restart = "time"
            case [False, False, False, True]:
                restart = "instructor"
            case [False, False, False, False]:
                pass
            case [True, False, True, False]:
                # Room with day is exhausted
                restart = "room and day"
            case _:
                print("Unknown", [r_restart, d_restart, t_restart, i_restart])
                exit()
        return {"i": instructor, "r": room, "d": day, "t": time}, restart

    def next_instructor(self, array: List[Instructor], index: int | None):
        restart = False
        if index >= len(array):
            restart = True
            return array[0], restart
        
        return array[index], restart
    
    def next_room(self, array: List[Room], index: int):
        restart = False
        if index >= len(array):
            restart = True
            return array[0], restart
        return array[index], restart
    
    def next_day(self, array: List[Day], index: int):
        restart = False
        if index >= len(array):
            restart = True
            return array[0], restart
        return array[index], restart
    
    def next_time(self, array: List[Time], index: int):
        restart = False
        if index >= len(array):
            restart = True
            return array[0], restart
        return array[index], restart

    

        


    