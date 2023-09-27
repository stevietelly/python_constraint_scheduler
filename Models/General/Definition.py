
from typing import List

from Logic.Structure.Variables import Static
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor



class Definition:
    def __init__(self, reader_output: dict) -> None:
        self.reader_output = reader_output
        self.statics: List[Static] =  list()
      
        self.StaticSetting()
    
    def StaticSetting(self):
        index = 1
        for programme in self.reader_output["programmes"]:
            programme: Programme = programme
            for group in programme.groups:
                for unit_identifier in group.units:
                    unit =  self.get_unit(unit_identifier)
                    instructor_identifier = unit.qualified_instructors[0]
                    instructor = self.get_instructor(instructor_identifier)
                    self.statics.append(Static(unit, group, instructor))
                    index += 1

    def get_unit(self, identifier: int)->Unit:
        for unit in self.reader_output["units"]:
            if unit.identifier == identifier:
                return unit
    
    def get_instructor(self, identifier: int)->Instructor:
        for instructor in self.reader_output["instructors"]:
            if instructor.identifier == identifier:
                return instructor
    

    def Output(self):
        return self.statics   