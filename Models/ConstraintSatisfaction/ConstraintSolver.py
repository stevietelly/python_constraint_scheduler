from typing import List
from Errors.Exception import NoValueFound

from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain
from Models.General.Reductions import PreferencesReduction


class ConstraintSolver:
    def __init__(self, statics: List[Static], reader_output: dict) -> None:
        self.statics =  statics
        self.reader_output = reader_output
        self.domain = Domain(self.statics, None)
        self.assignment = Assignment(self.statics, {"room": None, "daytime": None})
    
    def NodeConsistency(self):
        values = {
            "room": self.reader_output["rooms"],
            "daytime": self.reader_output["configuration"].timelines["daytimes"]}
        
        for static in self.statics:
            unit_values, _ = PreferencesReduction(static.unit.preferences, values).Reduce()
            group_values, _ = PreferencesReduction(static.group.preferences, unit_values).Reduce()
            instructor_values, _ = PreferencesReduction(static.instructor.preferences, group_values).Reduce()

          
            instructor_values["room"] = [room for room in instructor_values["room"] if room.capacity >= static.group.total]
            if instructor_values["room"] == []: raise NoValueFound(static, "room")
            if instructor_values["daytime"] == []: raise NoValueFound(static, "daytime")

            
            aggregated_values = [{"room": room, "daytime": daytime} for room in instructor_values["room"] for daytime in instructor_values["daytime"]]
        
            self.domain.set_value(static, aggregated_values)

  


    def Backtrack(self):
        if self.assignment.is_complete(): return self.assignment

        variable = self.assignment.select_unnasigned()
        values = self.domain.get_value(variable)

        for value in values:
            if self.assignment.check_if_consistent(value):
                self.assignment.set_value(variable, value)
                result = self.Backtrack()
                if result is not None: return result

        return None

            