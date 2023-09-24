from Logic.DateTime.Day import Day
from Logic.DateTime.Time import Time


print(Day("Monday", Time("0:00am"), Time("0:00am")) > Day("Tuesday", Time("0:00am"), Time("0:00am")))