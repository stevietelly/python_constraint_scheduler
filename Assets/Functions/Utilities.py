from typing import *
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Duration import Duration

from Logic.DateTime.Time import Time
def return_list_of_days(days: List[str], start_time: Time, end_time: Time)-> List[Day]:
    """
    Return a list of day objects with a listc of days in strings and the start time and end time for a day
    """
    return_list = []
    
    for day in days:
        conf_day = Day(day, start_time, end_time)
        conf_day.days = days
        return_list.append(conf_day)
    return return_list

def return_list_of_daytimes(days: List[Day], times: List[Time]):
    """
    Return a list of daytimes
    """
    daytimes = []
    for day in days:
        for time in times:
            daytimes.append(DayTime(day, time))
    return daytimes

def return_list_of_times(start_time: Time, end_time: Time, duration: int):
    """
    Retuen a list of division of times in a day based on the start time and duration
    """

    times = []
    current_time = start_time
    while end_time != current_time:   
        times.append(current_time)
        current_time += Duration(duration, 0)
    times.append(current_time)
    return times
