
from typing import List, Tuple
from Assets.Functions.Echo import Echo

from Data.Parser.Reader import ReaderOutput
from Logic.Structure.Variables import Dynamic, Static




class Definition:
    """
    Problem Definition
    - Breaking Down all the available objects into two types of variables
        1. Static Variables
        2. Dynamic Variables
    
    How the two are made is completely dependent on Wheteher or not the algorithm can choose instructors

    PARAMS:
        - reader_output: `ReaderOutput`
        - choose_instructors: `bool` 
    """
    def __init__(self, reader_output: ReaderOutput, choose_instructors: bool=False) -> None:
        echo = Echo()
        echo.print("\nProblem Definition", color="magenta")
        self.reader_output: ReaderOutput = reader_output
        self.statics: List[Static] =  list()
        self.choose_instructors = choose_instructors
        self.dynamic_variables: List[Dynamic] = list()
        self.StaticSetting()
        self.DynamicSetting()

    def StaticSetting(self):
        # Create The Different Static Variables
        for group in self.reader_output.groups:
            for unit_identifier in group.units:
                unit = self.get_unit(unit_identifier)
                instructor_identifier = unit.qualified_instructors[0]
                instructor = self.get_instructor(instructor_identifier) if self.choose_instructors else None
                s = Static(unit, group, instructor)
                if not self.choose_instructors: s.instructor = instructor
                self.statics.append(s)

    def DynamicSetting(self):
        for static in self.statics:
            instructors = [self.get_instructor(static.unit.qualified_instructors[0])] if not self.choose_instructors else [self.get_instructor(i) for i in static.unit.qualified_instructors]
            self.dynamic_variables.append(Dynamic(self.reader_output.times, self.reader_output.days,self.reader_output.rooms, instructors))

    def get_unit(self, identifier: int):
        for unit in self.reader_output.units:
            if unit.identifier == identifier:
                return unit

    def get_instructor(self, identifier: int):
        for instructor in self.reader_output.instructors:
            if instructor.identifier == identifier:
                return instructor

    def Output(self)->Tuple[List[Static], List[Dynamic]]:
        return self.statics, self.dynamic_variables 
 