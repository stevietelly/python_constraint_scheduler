from os import path
import re
from Assets.Functions.Utilities import generate_days
from Data.Validators.Structure import VALID_FILE_FOMARTS, ALGORITHMS
from Logic.DateTime.Week import Week


def confirm_file_path(input_str:str)->bool:
    return  path.isfile(input_str)

def is_valid_time(time_str:str)->bool:
    """
    Returns True if the given time string is a valid time, and False otherwise.
    Supports the following time formats: 
        1. HH:MM
        2. H:MM
        3. HH
        4. H
        5. HH:MMam/pm
        6. H:MMam/pm
    """
    time_regex = r'^(\d{1,2})(:(\d{2}))?([ap]m)?$'
    match = re.match(time_regex, time_str, re.IGNORECASE)
    if match is None:
        return False
    hour = int(match.group(1))
    minute = int(match.group(3)) if match.group(3) is not None else 0
    am_pm = match.group(4)
    if am_pm is not None:
        if hour == 0 or hour > 12:
            return False
        if am_pm.lower() == 'pm' and hour != 12:
            hour += 12
    else:
        if hour < 0 or hour > 23:
            return False
    if minute < 0 or minute > 59:
        return False
    return True
    

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def is_valid_day(day:str)->bool:
    if day.lower() in days:
        return True
    return False

def return_list_of_days(start_day:str, number_of_days:int)-> Week:
    return generate_days(start_day, int(number_of_days))

def is_valid_formart(formart:str):
    if formart in VALID_FILE_FOMARTS:
        return True
    return False

def algorithm_type_validator(algo: str) -> bool:
    if algo not in ALGORITHMS:
        return False
    return True