from typing import List
from Logic.DateTime.Time import Time



class Day:
    week = None
    days: List[str] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # TODO: Do not forget to insert this value
    def __init__(self, name: str, start: Time, end: Time):
       
        self.name = name.lower()
        self.index = self.days.index(self.name)
        self.start_time: Time = start
        self.end_time: Time = end
    
    def __add__(self, other: int):
        if isinstance(other, int):
            new_index = (self.days.index(self.name) + other) % len(self.days)
            return Day(self.days[new_index], self.start_time, self.end_time)
        raise TypeError("unsupported operand type(s) for +: 'Day' and '{}'".format(type(other).__name__))
    
    def __sub__(self, other: int):
        if isinstance(other, int):
            new_index = (self.days.index(self.name) - other) % len(self.days)
            return Day(self.days[new_index], self.start_time, self.end_time)
        raise TypeError("unsupported operand type(s) for +: 'Day' and '{}'".format(type(other).__name__))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Day:->{self.name.capitalize()}'
    
    def __eq__(self, other: object) -> bool:
        
        if not isinstance(other, Day): return False
        return  self.name.lower() == other.name.lower()     

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Day): return False
        return  self.name.lower() != other.name.lower()
        
    def __gt__(self, other: object):
        if not isinstance(other, Day): return False
        if self == other: return False
        return self.index > other.index
    
    def __lt__(self, other: object):
        if not isinstance(other, Day): return False
        if self == other: return False
        return self.index < other.index
   
          
    

    


    
   