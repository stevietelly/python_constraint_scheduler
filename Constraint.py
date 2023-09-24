from copy import deepcopy
from typing import Dict, List
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import Timetable
from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.ArcConsistency import ArcConsistency
from Models.ConstraintSatisfaction.Backtrack import Backtrack
from Models.ConstraintSatisfaction.Domain import Domain
from Models.ConstraintSatisfaction.NodeConsistency import NodeConsistency
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit

d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()


class ConstraintSolver:
    def __init__(self, reader_output) -> None:
        self.reader_output = reader_output
        self.domain: Domain
        self.statics: List[Static] = list()
        # self.domains: Dict[str, Domain] = {"unit": Domain, "group": Domain, "room": Domain, "instructor": Domain}
        self.domains: Dict[str, Domain] = {"room": Domain}
        self.global_resources = {
            "daytime": reader_output["configuration"].timelines["daytimes"],
            "room": reader_output["rooms"],
            "instructor": reader_output["instructors"],
            "unit": reader_output["units"],
            "group": reader_output["groups"]}

    def StaticSetting(self):
        index = 1
        for programme in self.reader_output["programmes"]:
            programme: Programme = programme
            for group in programme.groups:
                for unit_identifier in group.units:
                    unit =  self.get_unit(unit_identifier)
                    self.statics.append(Static(unit, group))

                    index += 1
    
    def get_unit(self, identifier: int)->Unit:
        for unit in self.reader_output["units"]:
            if unit.identifier == identifier:
                return unit
    
    def NodeConsistency(self):
        self.group_node_consistency()
        self.unit_node_consistency()
        self.room_node_consistency()
        self.instructor_node_consistency()

    def instructor_node_consistency(self):
        # instructor consistsency
        resources = deepcopy(self.global_resources)
        resources.pop("instructor")

        node  = NodeConsistency(self.reader_output, self.reader_output["instructors"], resources, type_="instructor")
        node.Consistency()
        self.domains["instructor"] = deepcopy(node.Output())

    def room_node_consistency(self):

        resources = deepcopy(self.global_resources)
        resources.pop("room")
      

        
        node = NodeConsistency(self.reader_output, self.reader_output["rooms"], resources, type_="room")
        node.Consistency()
        self.domains["room"] = deepcopy(node.Output())

    def unit_node_consistency(self):
        # unit consistsency
        resources = deepcopy(self.global_resources)
        resources.pop("unit")
        resources.pop("group")

        node = NodeConsistency(self.reader_output, self.reader_output["units"], resources, type_="unit")
        node.Consistency()
        self.domains["unit"] = deepcopy(node.Output())

    def group_node_consistency(self):
        # unit consistsency
        resources = deepcopy(self.global_resources.copy())
        resources.pop("unit")
        resources.pop("group")

        node = NodeConsistency(self.reader_output, self.reader_output["groups"], resources, type_="group")
        node.Consistency()
        self.domains["group"] = deepcopy(node.Output()) 

    def arc_consistency(self):
       
        ac = ArcConsistency(self.statics, {"unit": self.domains["unit"], "group": self.domains["group"]})
        ac.DomainHandling()
        ac.arc_handling()

        self.assignment = ac.assignment
        self.unit_group_domain = ac.domain
    
    def backtrack(self):
        b = Backtrack(self.assignment, self.unit_group_domain, {"room": self.domains["room"], "instructor": self.domains["instructor"]})
        assignment = b.Initialise()

        # timetable = Timetable(assignment.Output())
        # Write("", "timetable.json", timetable).dump()
        # assignment.Output()
        
        



cs = ConstraintSolver(reader_output)
cs.NodeConsistency()

cs.StaticSetting()

cs.arc_consistency()
cs.backtrack()
# Write("", "analyse.json", {"groups": cs.ac.domain.serial()}).dump()
