from Logic.Statistics.Costs.Cost import ClashCost, PreferenceSatisfacionCost
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from Logic.DateTime.DayTime import DayTime
from Objects.Academic.Units import Unit


class Session:
    """
    Represents a complete unit of a timetable
    """
    def __init__(self, identifier: int, group: Group, unit: Unit, instructor: Instructor, daytime: DayTime, room: Room) -> None:
        self.identifier =  identifier
        self.group = group
        self.unit = unit
        self.instructor = instructor
        self.daytime = daytime
        self.room = room

        self.resources = {
            "room": self.room,
            "group": self.group,
            "instructor": self.instructor
        }
        self.preference_satisfcation_cost: PreferenceSatisfacionCost = None
        self.clash_cost: ClashCost = ClashCost(0)
        self.room_capacity_cost = None
   
    
    def serialize(self):
        return {
            "identifier": self.identifier,
            "group": self.group.identifier,
            "unit": self.unit.identifier,
            "day": str(self.daytime.day),
            "time": str(self.daytime.time),
            "room": self.room.identifier,
            "instrcutor": self.instructor.identifier,
            "preference_satisfaction": self.preference_satisfcation_cost.value,
            "clash_cost": self.clash_cost.value,
            "room_capacity": self.room_capacity_cost.value
        }
    
    def AddClashCost(self, clash_cost: ClashCost):
        if self.clash_cost is None:
            self.clash_cost = clash_cost
        else:
            self.clash_cost += clash_cost
            
    def __repr__(self) -> str:
        return str(self)
    def __str__(self) -> str:
        return f"{self.group} taking {self.unit} in {self.room} with {self.instructor} at {self.daytime}"