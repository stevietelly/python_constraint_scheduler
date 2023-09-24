from typing import Dict, List,Tuple
from Logic.Structure.Variables import Static, Dynamic
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.Domain import Domain


class ArcConsistency:
    def __init__(self, statics: List[Static], unit_and_group_domains: Dict[str, Domain]) -> None:
        self.statics = statics
        self.domains = unit_and_group_domains
        
        self.assignment = Assignment(self.statics)
        self.domain: Domain = Domain(statics, None)

        self.arcs: List[Tuple[Static, Static]] = list()
        
    
    def DomainHandling(self):
        for static in self.statics:
            unit_values = self.domains["unit"].get_value(static.unit)
            group_values = self.domains["group"].get_value(static.group)
            intersecting_values = self.normalize_values(unit_values, group_values)
            
            self.domain.set_value(static, intersecting_values)

    def arc_handling(self):
        for static1 in self.statics:
            for static2 in self.statics:
                if static1 != static2 and (static1, static2) not in self.arcs:
                    self.arcs.append((static1, static2))
    def Revise(self, x, y):
        revised = False

    def Consistency(self):
        for arc in self.arcs:
            for x in self.domain.get_value(arc[0]):
                pass
  

    
    @classmethod
    def normalize_values(cls, unit_values, group_values):
        intersecting_values = unit_values.copy()
        for key in unit_values:
            intersecting_values[key] = [singular for singular in unit_values[key] if singular in group_values[key]]
        return intersecting_values
        