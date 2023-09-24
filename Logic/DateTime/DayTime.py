from Logic.DateTime.Day import Day
from Logic.DateTime.Time import Time


class DayTime:
    """
        A combination of day and timefor easy use
    """
    def __init__(self, day: Day, time: Time):
      
        self.day: Day = day
        self.time: Time = time
        self.format()

    def format(self):
        self.day_name = self.day.name
        self.time_string = self.time.time_string

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.day.name} at {self.time.hour}:{self.time.minuteHandling(self.time.minute)}{self.time.state}'

    def __eq__(self, other):
        if isinstance(other, DayTime):
            return self.day == other.day and self.time == other.time
        return False
        

    def __ne__(self, other):
        if isinstance(other, DayTime):
            return self.day != other.day or self.time != other.time
        return False

    def __lt__(self, other):
        print(self, other)
        if not isinstance(other, DayTime): return False
        return self.day < other.day or self.time < other.time

    # def __le__(self, other):
    #     if isinstance(other, DayTime):
    #         if self.day != other.day:
    #             return self.day < other.day
            
    #         return self.time <= other.time
    #     return False

    def __gt__(self, other):
      
        if not isinstance(other, DayTime): return False
        return self.day > other.day or self.time > other.time
            
        

    # def __ge__(self, other):
    #     if isinstance(other, DayTime):
    #         if self.day != other.day:
    #             return self.day > other.day
    #         else:
    #             return self.time >= other.time
    #     return NotImplemented

    # Define the __hash__() method
    def __hash__(self):
        # Use a tuple of the instance's attributes to compute its hash value
        return hash((self.day_name, self.time_string))
