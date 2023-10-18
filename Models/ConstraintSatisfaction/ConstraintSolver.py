from copy import deepcopy
from typing import List
from Assets.Functions.Echo import Echo
from Errors.Exception import NoAssignmenetPossible, NoValueFound

from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain
from Models.General.Reductions import PreferencesReduction
from Objects.Internal.Preference.Lookup import LookupInstructor
from Objects.Internal.Preference.Preference import Only

echo = Echo()

class ConstraintSolver:
    def __init__(self, statics: List[Static], reader_output: dict, **kwargs) -> None:
        """"
        search_rearangement_method:bool=False, choose_instructors: bool=False
        """
        self.statics =  statics
        self.reader_output = deepcopy(reader_output)
        self.domain = Domain(self.statics, None)
        self.srm = kwargs["search_rearangement_method"] if "search_rearangement_method" in kwargs.keys() else False
        self.choose_instructors = kwargs["choose_instructors"] if "choose_instructors" in kwargs.keys() else False
        self.srm_criteria = kwargs["search_rearangement_criteria"] if "search_rearangement_criteria" in kwargs.keys() else "least"
        self.assignment = Assignment(self.statics, {"room": None, "daytime": None}) if not self.choose_instructors else Assignment(self.statics, {"room": None, "daytime": None, "instructor": None})

        echo.print("\nSolving using Constraint Satisfaction ", color="magenta")
        if self.srm: echo.print(f"Instantiating Variables with {self.srm_criteria} number of variables.", color="yellow")
        if self.choose_instructors: echo.print("Instructors to be Picked by Algorithim, Non defined Instructors.", color="yellow")
    
    def NodeConsistency(self):
        echo.print("Node Consistency", color="green")
        values = {
            "room": self.reader_output["rooms"],
            "daytime": self.reader_output["configuration"].timelines["daytimes"],
            "instructor": self.reader_output["instructors"]}
        if not self.choose_instructors: values.pop("instructor")
        
        for static in self.statics:
            vls =  values
            vls, _ = PreferencesReduction(static.unit.preferences, vls).Reduce()
            vls, _ = PreferencesReduction(static.group.preferences, vls).Reduce()
            if not self.choose_instructors: vls, _ = PreferencesReduction(static.instructor.preferences, vls).Reduce()

            # Reduce instructors to only the accepted list per unit
            if self.choose_instructors:
                lookup_instrcutors = [LookupInstructor(inst_identifier) for inst_identifier in static.unit.qualified_instructors ]
                vls, _ = PreferencesReduction(Only(*lookup_instrcutors), vls).Reduce()
          
            vls["room"] = [room for room in vls["room"] if room.capacity >= static.group.total]

            for k, v in vls.items():
                if v == []: raise NoValueFound(static, k)
           
      
            aggregated_values = [{"room": room, "daytime": daytime} for room in vls["room"] for daytime in vls["daytime"]] if not self.choose_instructors else [{"room": room, "daytime": daytime, "instructor": instructor} for room in vls["room"] for daytime in vls["daytime"] for instructor in vls["instructor"]]
      
            self.domain.set_value(static, aggregated_values)

    def Backtrack(self):
        echo.print("Starting Backtracking", color="green")
        return self._backtrack()

    def _backtrack(self):
        if self.assignment.is_complete(): return self.assignment
        variable = self.select_next_variable()
    
        values = self.domain.get_value(variable)
        for value in values:
            if self.assignment.check_if_consistent(variable, value):
                self.assignment.set_value(variable, value)
                return self._backtrack()

        raise NoAssignmenetPossible(f"Unable to find a value for variable '{variable}'")
        
    def select_next_variable(self):
        if not self.srm: return self.assignment.select_unnasigned()
        all_variables_filtered = self.domain.all_variables_ascending_values() if self.srm_criteria == "least" else self.domain.all_variables_descending_values()
        last_assigned = self.assignment.last_assigned
        if last_assigned is None: return all_variables_filtered[0]
        index = all_variables_filtered.index(last_assigned)
        return all_variables_filtered[index + 1]
        
    def select_next_value(self, variable: Static):
        echo =  Echo()
        values: list = self.domain.get_value(variable)

        if not self.assignment.check_if_assigned(variable): return values[0]

        current_value = self.assignment.get_value(variable)
        index = values.index(current_value)
        if index + 1 >= len(values): echo.exit("Could not find next value")
        return values[index + 1]

