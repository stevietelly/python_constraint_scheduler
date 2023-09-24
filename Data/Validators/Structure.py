"""
This module validates the structure of the input data 
"""
from typing import List

CONFIGURATION = {
    "name": str,
    "days": list,
    "start_time": str,
    "end_time": str,
    "duration_per_session": int,
    "total_duration_for_sessions": int,
    "soft_contraints_satisfaction_rate": int,
    # a percentage rate
    "consecutive": {
        "room": int,
        "instructors": int,
        "units": int,
        "groups": int
    },
    "system": {
        "limit": int,
        "saturation": bool,
        "tries": int
    }
}

ROOM = {"identifier": int, "title": str, "capacity": int, "preferences": list | None}
PROGRAMME = {
    "identifier": int,
    "title": str,
    "levels": int,
}
GROUP = {"identifier": int, "title": str, "level": int, "total": int, "preferences": list | None}
INSTRUCTOR = {
    "identifier": int,
    "name": str,
    "title": str,
    "gender": str,
    "preferences": list | None
}
SESSION = {
    "identifier": int,
    "room": int,
    "day": str,
    "time": str,
    "schedule" : {
        "identifier": int,
        "unit": int,
        "instructor": int,
        "group": int
    }
}

UNIT = {
    "identifier": int,
    "sessions": int,
    "title": str,
    "qualified": list,
    "preferences": list | None
}

VALID_FILE_FOMARTS = ["json", "txt"]

VALID_INPUT_FILE_FOMARTS = ["json", "txt"]

VALID_OUTPUT_FILE_FOMARTS = ["json"]

INPUT_FILE_UNITS = ["configuration", "instructors", "units", "programmes", "rooms", "groups"]

INPUT_FILE_STRUCTURE = {"configuration": CONFIGURATION, "instructors": INSTRUCTOR, "units": UNIT, "programmes": PROGRAMME, "rooms": ROOM, "groups": GROUP}

ALGORITHMS = ["constraint_satisfaction", "genetic", "annealing"]

VALID_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
