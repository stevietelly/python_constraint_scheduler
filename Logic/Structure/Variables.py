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
    def __init__(self,unit: Unit, group: Group, instructor: Instructor):
        
        self.unit: Unit = unit
        self.group: Group = group
        self.instructor: Instructor = instructor
       

    def __str__(self):
        return f'{self.group} taking {self.unit} with {self.instructor}'

    def __repr__(self):
        return f'StaticVariable({self.group} taking {self.unit})'
    
    def __eq__(self, static):
        if not isinstance(static, Static): return False
        return (self.group.identifier == static.group.identifier) and (self.unit.identifier == static.unit.identifier) and (self.instructor.identifier == static.instructor.identifier)
    
    def __ne__(self, static):
        if not isinstance(static, Static): return False
        return (self.group.identifier != static.group.identifier) and (self.unit.identifier != static.unit.identifier) and (self.instructor.identifier != static.instructor.identifier)
        
    
 

class Dynamic:
    def __init__(self, time: Time, day: Day, room: Room) -> None:
        
        self.time: Time = time
        self.Day: Day = day
        self.room: Room = room

    def __str__(self):
        return f'DynamicVariable({self.room} at {DayTime(self.day, self.time)})'
    
    def __eq__(self, dynamic):
        if not isinstance(dynamic, Dynamic): return False
        return (self.time == dynamic.time) and (self.day == dynamic.day) and (self.room == dynamic.room)
    
    def __ne__(self, dynamic) -> bool:
        if not isinstance(dynamic, Dynamic): return False
        return (self.time != dynamic.time) and (self.day != dynamic.day) and (self.room != dynamic.room)
    

        
 