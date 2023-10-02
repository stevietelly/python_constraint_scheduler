from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from Logic.DateTime.DayTime import DayTime
from Objects.Academic.Units import Unit


class Session:
    def __init__(self, identifier: int, group: Group, unit: Unit, instructor: Instructor, daytime: DayTime, room: Room) -> None:
        self.identifier =  identifier
        self.group = group
        self.unit = unit
        self.instructor = instructor
        self.daytime = daytime
        self.room = room
    
    def serialize(self):
        return {
            "identifier": self.identifier,
            "group": self.group.identifier,
            "unit": self.unit.identifier,
            "day": str(self.daytime.day),
            "time": str(self.daytime.time),
            "room": self.room.identifier,
            "instrcutor": self.instructor.identifier
        }