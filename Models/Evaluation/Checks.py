from typing import List
from Logic.DateTime.DayTime import DayTime
from Models.General.Reductions import PreferencesReduction

from Objects.Internal.Preference.Preference import Rule
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room


class RuleCheck:
    def __init__(self, rule: Rule, session_daytime: DayTime, session_room: Room, session_instructor: Instructor, reader_output) -> None:
        self.rule = rule
        self.daytime = session_daytime
        self.room = session_room
        self.instructor = session_instructor
        self.reader_output = reader_output

    def Evaluate(self):
        timelines = self.reader_output["configuration"].timelines["daytimes"]
        rooms = self.reader_output["rooms"]
        instructors = self.reader_output["instructors"]
        values = {"daytime": timelines, "room": rooms, "instructor": instructors}


        p = PreferencesReduction(self.rule, values)
        final_values, change = p.Reduce()
        
        return self.daytime in final_values["daytime"] and self.instructor in final_values["instructor"] and self.room in final_values["room"]
      