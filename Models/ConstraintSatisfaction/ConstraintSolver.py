from copy import deepcopy
from typing import List
from Assets.Functions.Echo import Echo
from Errors.Exception import NoAssignmenetPossible
from Logic.Structure.Variables import Dynamic, Static, Value
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain
from Models.General.Reductions import PreferencesReduction
from Objects.Internal.Preference.Preference import All, And

echo = Echo()
class ConstraintSolver:
    """
    A class for the constraint staisfaction algorithim

    Attributes
    ---------
    `statics` : List[Statics]
        changing variables

    `search_rearangement_method`: bool 
        - Instatinating Variable in a sepecific order
        - default is False

    `search_rearangement_criteria` : str
        - The order in which variables will be instantiated
        - deafault is 'least'
        - only options are 'most', 'least' anything else will be considered 'most'

    """
    def __init__(self, statics: List[Static], dynamics: List[Dynamic], **kwargs) -> None:
        self.srm = kwargs["search_rearangement_method"] if "search_rearangement_method" in kwargs.keys() else False
        self.choose_instructors = kwargs["choose_instructors"] if "choose_instructors" in kwargs.keys() else False
        self.srm_criteria = kwargs["search_rearangement_criteria"] if "search_rearangement_criteria" in kwargs.keys() else "least"
        self.assignment = Assignment(statics, Value())
        self.domain = Domain(statics, dynamics)

        # Echo Functionality
        echo.print("\nSolving using Constraint Satisfaction ", color="magenta")
        if self.srm: echo.print(f"Instantiating Variables with {self.srm_criteria} number of variables.", color="yellow")
        if self.choose_instructors: echo.print("Instructors to be Picked by Algorithim, Non defined Instructors.", color="yellow")

    def NodeConsistency(self):
        echo.print("Node Consistency", color="green")
        for static in self.domain.variables:
            preferences = And(*[static.group.preferences, static.unit.preferences, static.instructor.preferences if not static.instructor is None else All()])
            dynamic_variable = deepcopy(self.domain.get_values(static))
            PreferencesReduction(preferences, dynamic_variable).Reduce()
            self.domain.set_dynamic_variable(static, dynamic_variable)
            
    def Backtrack(self):
        echo.print("Starting Backtracking", color="green")
        self._backtrack()

    def _backtrack(self):
        if self.assignment.is_complete(): return self.assignment
        next_variable: Static = self.get_next_variable()
        index = {"i": 0 , "r": 0, "dt": 0}
        while True:
            value, restart = self.domain.get_next_value(next_variable, index)
            if restart:
                if restart == "daytime":
                    index["dt"] = 0
                    index["r"] += 1
                elif restart == "room":
                    index["r"] = 0
                    index["dt"] += 1
                else:
            
                    raise NoAssignmenetPossible(f"No more Resources for {next_variable} restart required for {restart}")
            else:

                is_consistent, consistency_problem = self.assignment.check_if_consistent(next_variable, value)
                if not is_consistent:
                    if consistency_problem == "room":
                        index["dt"] += 1
                    elif consistency_problem == "instructor":
                        index["dt"] += 1
                    elif consistency_problem == "all":
                        index["dt"] += 1
                        index["r"] += 1
                    elif consistency_problem == "group":
                        index["dt"] += 1
                    else:
                        echo.exit("Consistency Problem for", consistency_problem)
                else:
                    v = Value()
                    v.instructor = value["i"]
                    v.room = value["r"]
                    v.day = value["dt"].day
                    v.time = value["dt"].time
                    v.instructor = value["i"]
                    self.assignment.set_value(next_variable, v)
                    return self._backtrack()

    def get_next_variable(self):
        if not self.srm: return self.assignment.select_unassigned()
        unnasigned = self.assignment.all_unassigned()
        lengths = []
        for index in unnasigned:
            lengths.append((index, len(self.domain.values[index])))
        criteria = False if self.srm_criteria == "least" else True
        lengths.sort(key=lambda item: item[1], reverse=criteria)
        return self.assignment.get_static_by_index(lengths[0][0])
 