from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class Static:
    """
    A static Variable holds unchanging components that have to exist
    
    
    """
    def __init__(self,unit: Unit, group: Group):
        
        self.unit: Unit = unit
        self.group: Group = group
       

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'StaticVariable({self.group} taking {self.unit})'
    
    def __eq__(self, static):
        return (self.group == static.group) and (self.unit == static.unit)
    
    def __ne__(self, static):
        return (self.group != static.group) and (self.unit != static.unit)
    
 

class Dynamic:
    def __init__(self, instructor: Instructor, time: Time, day: Day, room: Room) -> None:
        
        self.instructor: Instructor = instructor
        self.time: Time = time
        self.Day: Day = day
        self.room: Room = room

    def __str__(self):
        return f'DynamicVariable:->{self.instructor} in {self.room} at {DayTime(self.day, self.time)}'
    
    def __eq__(self, static):
        return (self.static_variables == static.static_variables) and (self.inst == static.unit)
    
 