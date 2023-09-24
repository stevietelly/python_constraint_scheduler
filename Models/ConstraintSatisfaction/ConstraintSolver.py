from typing import Dict, Any, List
from Logic.Structure.Session import Session
from Logic.Structure.Variables import Dynamic, Static
from Models.ConstraintSatisfaction.Assignment import Assignment

from Models.ConstraintSatisfaction.Domain import Domain
from Models.ConstraintSatisfaction.NodeConsistency import NodeConsistency
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Students import Group


class ConstraintSolver:
    def __init__(self, reader_output) -> None:
        self.reader_output = reader_output
    
        self.global_resources = {
            "daytime": reader_output["configuration"].timelines["daytimes"],
            "room": reader_output["rooms"],
            "instructor": reader_output["instructors"],
            "unit": reader_output["units"],
            "group": reader_output["groups"]}
        self.empty_resources = {
            "daytime": [],
            "room": [],
            "instructor": [],
            "unit": [],
            "group": []}
        self.domains: Dict[str, Domain] = dict().fromkeys(["unit", "instructor", "room", "group"])
        self.statics: List[Static] = list()
        self.assignment: Assignment
        self.sessions: List[Session] = list()

    def node_consistency(self):
        self.instructor_node_consistency()
        self.unit_node_consistency()
        self.room_node_consistency()
        self.group_node_consistency()
    
    def unit_node_consistency(self):
        # unit consistsency
        resources = self.global_resources.copy()
        resources.pop("unit")
        resources.pop("group")

        node = NodeConsistency(self.reader_output, self.reader_output["units"], resources, type_="unit")
        node.Consistency()
        self.domains["unit"] = node.Output() 
        
    def instructor_node_consistency(self):
        # instructor consistsency
        resources = self.global_resources.copy()
        resources.pop("instructor")

        node  = NodeConsistency(self.reader_output, self.reader_output["instructors"], resources, type_="instructor")
        node.Consistency()
        self.domains["instructor"] = node.Output()
    
    def group_node_consistency(self):
        # instructor consistsency
        resources = self.global_resources.copy()
        resources.pop("group")
        resources.pop("unit")

        node  = NodeConsistency(self.reader_output, self.reader_output["groups"], resources, type_="group")
        node.Consistency()
        self.domains["group"] = node.Output()
    
    def room_node_consistency(self):

        resources = self.global_resources.copy()
        resources.pop("room")

        
        node = NodeConsistency(self.reader_output, self.reader_output["rooms"], resources, type_="room")
        node.Consistency()
        self.domains["room"] = node.Output()

    def get_unit(self, identifier: int)->Unit:
        for unit in self.reader_output["units"]:
            if unit.identifier == identifier:
                return unit

    def StaticSetting(self):
        index = 1
        for programme in self.reader_output["programmes"]:
            programme: Programme = programme
            for group in programme.groups:
                for unit_identifier in group.units:
                    unit =  self.get_unit(unit_identifier)
                    self.statics.append(Static(unit, group))
                    index += 1
        self.assignment = Assignment(self.statics)
    
    def get_values(self, unit: Unit, group: Group):
        unit_values: dict = self.domains["unit"].get_value(unit)
        group_values = self.domains["group"].get_value(group)

        intersecting_values = {key: [value for value in unit_values[key] if value in group_values[key]] for key in unit_values.keys()}

        return intersecting_values

    def get_values_from_static(self, static_variable: Static):
        return self.get_values(static_variable.unit, static_variable.group)

    def AC_3(self):
        
        if self.assignment.is_complete(): return self.assignment
        
        unnasigned: Static = self.assignment.select_unnasigned()
        probable_values = self.get_values_from_static(unnasigned)

        # Daytime
        daytimes = probable_values["daytime"]
        next_daytime = self.next_value(daytimes, self.assignment.get_daytime(unnasigned))
        if next_daytime is None: print("no daytime")
        
        self.assignment.set_daytime(unnasigned, next_daytime)

        # Instructor
        instructors = probable_values["instructor"]
        next_instructor = self.next_value(instructors, self.assignment.get_instructor(unnasigned))
        self.assignment.set_instructor(unnasigned, next_instructor)

        # Room
        rooms = probable_values["room"]
        next_room = self.next_value(rooms, self.assignment.get_room(unnasigned))
        self.assignment.set_room(unnasigned, next_room)

        self.Revise(unnasigned)

        return self.AC_3()
    
    def next_value(self, list_of_items: list, current=None):
        if current is None: return list_of_items[0]
        index =  list_of_items.index(current) + 1
        if index > len(list_of_items): return None
        return list_of_items[index]
        
    def Revise(self, assigned: Static):
        chosen_values  = self.assignment.get_value(assigned)

        # choice_values = self.domains["instructor"].get_value(chosen_values["instructor"])["daytime"].remove(chosen_values["daytime"])
        # choice_values = self.domains["room"].get_value(chosen_values["room"])["daytime"].remove(chosen_values["daytime"])
        # print(choice_values)
        # exit()
        
    def Assesion(self):
        for static_variable in self.statics:
            values = self.assignment.get_value(static_variable)
            dynamic_variable = Dynamic(values["instructor"], values["daytime"].time, values["daytime"].day, values["room"])
            self.sessions.append(Session(static_variable, dynamic_variable))

    def Output(self):
        return self.sessions
        
            
   