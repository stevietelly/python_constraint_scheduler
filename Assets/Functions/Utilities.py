from typing import *
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Duration import Duration

from Logic.DateTime.Time import Time
from Logic.Structure.Session import Session
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



def sort_sessions_by_daytime(sessions: List[Session]) -> List[Session]:
    """
    Sorts a list of sessions using the merge sort algorithm based on their DayTime attribute.

    Args:
        sessions (List[Session]): The list of sessions to sort.

    Returns:
        List[Session]: The sorted list of sessions.
    """
    # Base case: If the list has one or fewer items, it is already sorted
    if len(sessions) <= 1:
        return sessions

    # Recursive case: Split the list in half and recursively sort each half
    mid = len(sessions) // 2
    left_half = sessions[:mid]
    right_half = sessions[mid:]
    left_sorted = sort_sessions_by_daytime(left_half)
    right_sorted = sort_sessions_by_daytime(right_half)

    # Merge the sorted halves into a single sorted list
    sorted_sessions = []
    i, j = 0, 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i].daytime <= right_sorted[j].daytime:
            sorted_sessions.append(left_sorted[i])
            i += 1
        else:
            sorted_sessions.append(right_sorted[j])
            j += 1
    sorted_sessions.extend(left_sorted[i:])
    sorted_sessions.extend(right_sorted[j:])
    return sorted_sessions

    