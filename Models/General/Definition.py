
from typing import List
from Assets.Functions.Echo import Echo
from Logic.Structure.Variables import Static




class Definition:
    """
        Problem Definition

        preparing the input
    """
    def __init__(self, reader_output: dict, choose_instructors: bool=False) -> None:
        echo = Echo()
        echo.print("\nProblem Definition", color="magenta")
        self.reader_output = reader_output
        self.statics: List[Static] =  list()
        self.choose_instructors = choose_instructors
        self.StaticSetting()
    
    def StaticSetting(self):
        for group in self.reader_output["groups"]:
            for unit_identifier in group.units:
                unit = self.get_unit(unit_identifier)
                # FIXME: Add an option to pick from a bunch of instructor
                instructor_identifier = unit.qualified_instructors[0]
                instructor = self.get_instructor(instructor_identifier)
                s = Static(unit, group)
                if not self.choose_instructors: s.instructor = instructor
                self.statics.append(s)
                    
    def get_unit(self, identifier: int):
        for unit in self.reader_output["units"]:
            if unit.identifier == identifier:
                return unit
    
    def get_instructor(self, identifier: int):
        for instructor in self.reader_output["instructors"]:
            if instructor.identifier == identifier:
                return instructor
    
    def Output(self):
        return self.statics  
 