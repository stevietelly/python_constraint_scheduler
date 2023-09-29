from copy import deepcopy
from typing import List
from Assets.Functions.Echo import Echo
from Errors.Exception import NoAssignmenetPossible, NoValueFound

from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain
from Models.General.Reductions import PreferencesReduction

echo = Echo()

class ConstraintSolver:
    def __init__(self, statics: List[Static], reader_output: dict, search_rearangement_method:bool=False) -> None:
        self.statics =  statics
        self.reader_output = reader_output
        self.domain = Domain(self.statics, None)
        self.srm = search_rearangement_method
        self.assignment = Assignment(self.statics, {"room": None, "daytime": None})

        echo.print("\nSolving using Constraint Satisfaction ", color="magenta")
    
    def NodeConsistency(self):
        echo.print("Node Consistency", color="green")
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
        echo.print("Staring Backtracking", color="green")
        return self._backtrack()

    def _backtrack(self):
        if self.assignment.is_complete(): return self.assignment
        variable = self.assignment.select_unnasigned()
        values = self.domain.get_value(variable)
        for value in values:
            if self.assignment.check_if_consistent(value):
                self.assignment.set_value(variable, value)
                return self._backtrack()

        raise NoAssignmenetPossible(f"Failed at finding a value for variable '{variable}'")
   
        
    def select_next_variable(self):
        if not self.srm: return self.assignment.select_unnasigned()
        all_variables_ascending_values = self.domain.all_variables_ascending_values()
        last_assigned = self.assignment.last_assigned
        if last_assigned is None: return all_variables_ascending_values[0]
        index = all_variables_ascending_values.index(last_assigned)
        return all_variables_ascending_values[index + 1]
        
    def select_next_value(self, variable: Static):
        echo =  Echo()
        values: list = self.domain.get_value(variable)

        if not self.assignment.check_if_assigned(variable): return values[0]

        current_value = self.assignment.get_value(variable)
        index = values.index(current_value)
        if index + 1 >= len(values): echo.exit("Could not find next value")
        return values[index + 1]
            