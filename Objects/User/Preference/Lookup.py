from Errors.Exception import InvalidTime
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time




class Lookup:
    """
    Lookups are the stepping stones for unary constraints conversion
    from Prefrences to Constrainsts
    """
    def __init__(self,string_type_: str, value) -> None:
       
        self.value = value
        self.string_type_ = string_type_
    
    def __repr__(self) -> str:
        return f"Lookup {self.string_type_}: {self.value}"

class LookupUnit(Lookup):
    """
    The lookup for unit
    """
    def __init__(self, identifier:int) -> None:
        super().__init__(string_type_="unit", value=identifier)
    
    def __eq__(self, __value: object) -> bool:
        return __value.identifier == int(self.value)
    
    def __ne__(self, __value: object) -> bool:
        return __value.identifier == int(self.value)
        
class LookupGroup(Lookup):
    """
    The lookup for group
    """
    def __init__(self, identifier:int) -> None:
        super().__init__(string_type_="group", value=identifier)      

class LookupTime(Lookup):
    """
    The lookup for time
    """
    def __init__(self, timestring: str) -> None:
        super().__init__(string_type_="time",  value=timestring)
        try:
            self.value=Time(timestring)
        except:
            raise InvalidTime(self.value)
        
class LookupRoom(Lookup):
    """
    The lookup for room
    """
    def __init__(self, identifier: str) -> None:
        super().__init__(string_type_="room", value=str(identifier))     

class LookupDayTime(Lookup):
    """
    The lookup for daytime
    """
    def __init__(self, time_string:str) -> None:
        super().__init__(string_type_="daytime", value=time_string)
        self.day_string, self.time_string = time_string.split(" at ")
        t = Time("0:00am")
        day, time = Day(self.day_string, t, t), Time(self.time_string)
        self.value = DayTime(day, time)
        
class LookupDay(Lookup):
    """
    The lookup for day
    """
    def __init__(self, day:str) -> None:
        super().__init__(string_type_="day", value=day)
        t = Time("0:00am")
        self.value = Day(day, t, t)
class LookupInstructor(Lookup):
    """
    Instructor Lookup
    """
    def __init__(self, value) -> None:
        super().__init__(string_type_="instructor", value =value)
        self.value = int(value)