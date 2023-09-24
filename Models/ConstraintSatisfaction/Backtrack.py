from copy import deepcopy
from typing import Dict
from Errors.Exception import NoValueFound
from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain


class Backtrack:
    def __init__(self, assignment: Assignment, global_domain: Domain, room_instructor_domains: Dict[str, Domain]) -> None:
        self.assignment = assignment
        self.global_domain = global_domain
        self.global_domain_copy = deepcopy(global_domain)

        self.room_instructor_domains = room_instructor_domains
    
   
    def Initialise(self, working_variable: Static | None = None, change: str | None=None):
        if self.assignment.is_complete(): return self.assignment
    
        variable = working_variable
        if working_variable is None: variable = self.assignment.select_unnasigned()
        values = self.global_domain.get_value(variable)

        if change is None:
            self.change_daytime(values, variable)
            self.change_room(values, variable)
            self.change_instructor(values, variable)
        elif change == "room":
            self.change_room(values, variable)
        elif change == "instructor":
            self.change_daytime(values, variable)
        elif change == "daytime":
            self.change_daytime(values, variable)
        else:
            print(change)
            exit()

        boolean, inconsistency = self.is_assignment_consistent()
        if boolean:
            return self.Initialise()
        return self.Initialise(self.assignment.select_last_assigned(), inconsistency)

        

        # if change is None:
        #     self.change_daytime(values, variable)
        #     self.change_room(values, variable)
        # elif change == "daytime":
        #     self.change_daytime(values, variable)
        # elif change == "room":
        #     self.change_room(values, variable)
       
        # boolean, inconsistency = self.is_assignment_consistent()
        # if not boolean:
        #     return self.Initialise(variable, inconsistency)
        # return self.Initialise(None, None)

    def change_daytime(self, values, variable):
        daytimes = values["daytime"]
        accepted_daytime = self.set_next_value(daytimes, self.assignment.get_daytime(variable))
        self.assignment.set_daytime(variable, accepted_daytime)

    def change_room(self, values, variable):
        rooms = values["room"]
        current_room = self.assignment.get_room(variable)
        accepted_room = self.set_next_value(rooms, current_room)
        self.assignment.set_room(variable, accepted_room)
    
    def change_instructor(self, values, variable):
        # FIXME: change how we get instructors
        for instructor in self.room_instructor_domains["instructor"].variables:
            if variable.unit.qualified_instructors[0] == instructor.identifier: self.assignment.set_instructor(variable, instructor)

    def is_assignment_consistent(self)->bool:
        """
        Check if the asignment is consitent
        Check if there are any clashes
        Typically
        if a room has been allocated a period in two different instances
        """
        last_assigned = self.assignment.select_last_assigned()
        values_of_last_assigned = self.assignment.get_value(last_assigned)
        print(values_of_last_assigned, last_assigned)
        if any([value == False for _, value in values_of_last_assigned.items()]): raise NoValueFound(last_assigned)


        for static_variable in self.assignment.static_variables:
            values = self.assignment.get_value(static_variable)
            
            if values["room"] == values_of_last_assigned["room"] and values["daytime"] == values_of_last_assigned["daytime"]: return False, "room"
            if values["instructor"] == values_of_last_assigned["instructor"] and values["daytime"] == values_of_last_assigned["daytime"]: return False, "instructor"
            if values == values_of_last_assigned: return False, "daytime"
            

        return True, None


    @classmethod
    def set_next_value(cls, list_of_values: list, current_value: None | str):
        
            if current_value is None: return list_of_values[0]
            index = list_of_values.index(current_value)
            if index + 1 >= len(list_of_values): return False
            return list_of_values[index+1]
        