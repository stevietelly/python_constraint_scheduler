from typing import List
from Assets.Functions.Echo import Echo
from Logic.Statistics.Calculators import GroupCalculator, InstructorCalculator, RoomCalculator
from Logic.Statistics.Costs.Cost import PreferenceSatisfacionCost, RoomCapacity
from Logic.Structure.Timetable import Timetable
from Models.Evaluation.Checks import RuleCheck
from Objects.Internal.Preference.Preference import All
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room

echo = Echo()
class FitnessEvaluation:
    """
    Fitness Evaluation
    
    This class checks how good a solution is in developing a complete
    timetable with no clashes.

    This is done by evaluating any clashes in groups, rooms and instructors,
    checking for preference staisfaction and room capacity adherance.

    Eventually, a score is given, contributing to how good the solution is. 

    NB: `Automatically Evaluates, no need to call Evaluate() method`

    """
    def __init__(self, timetable, reader_output) -> None:
        self.timetable: Timetable = timetable
        self.readerOutput = reader_output

        self.timelines = reader_output["configuration"].timelines
        self.groups: List[Group] = self.readerOutput["groups"]
        self.rooms: List[Room] = self.readerOutput["rooms"]
        self.instructors: List[Instructor] = self.readerOutput["instructors"]
        self.instructors: List[Instructor] = self.readerOutput["instructors"]
        self.instructors: List[Instructor] = self.readerOutput["instructors"]
        self.Evaluate()

    def Evaluate(self):
        echo.print("\nEvaluating Timetable.....", color="magenta")
        self.evaluate_clashes()
        self.evaluate_preferences()
        self.evaluate_room_capacity()
        self.timetable.evaluated = True

    def evaluate_clashes(self):
        echo.print("Evaluating Clashes", color="green")
        self.evaluate_group_clashes()
        self.evaluate_instructor_clashes()
        self.evaluate_group_clashes()

    def evaluate_group_clashes(self):
        clashes = []
        for group in self.groups:
            calculator = GroupCalculator(group, self.timelines["daytimes"])
            sessions = self.timetable.GetAllSessionByGroup(group.identifier)
            calculator.AddSessions(*sessions)
            calculator.Analyse()
            clashes.extend(calculator.clashes)
        self.timetable.clashes[calculator.type_] = clashes

    def evaluate_room_clashes(self):
        for room in self.rooms:
            calculator = RoomCalculator(room, self.timelines["daytimes"])
            sessions = self.timetable.GetAllSessionByRoom(room.identifier)
            calculator.AddSessions(*sessions)
            calculator.Analyse()
            self.timetable.clashes[calculator.type_].extend(calculator.clashes)

    def evaluate_instructor_clashes(self):
        for instructor in self.instructors:
            calculator = InstructorCalculator(instructor, self.timelines["daytimes"])
            sessions = self.timetable.GetAllSessionByInstructor(instructor.identifier)
            calculator.AddSessions(*sessions)
            calculator.Analyse()
            self.timetable.clashes[calculator.type_].extend(calculator.clashes)
    
    def evaluate_preferences(self):
        echo.print("Evaluating Preferences", color="green")
        for index, session in enumerate(self.timetable.sessions):
            preferences = []
            if not isinstance(session.instructor.preferences, All):preferences.append(session.instructor.preferences)
            if not isinstance(session.group.preferences, All):preferences.append(session.group.preferences)
            if not isinstance(session.room.preferences, All):preferences.append(session.room.preferences)
            if not isinstance(session.unit.preferences, All):preferences.append(session.unit.preferences)
            if not preferences:
                total = len(preferences)
                false_count = 0
                for preference in preferences:
                    r = RuleCheck(preference, session.daytime, session.room, session.instructor, self.readerOutput)
                    boolean = r.Evaluate()
                    if not boolean: false_count += 1
                p = PreferenceSatisfacionCost(total-false_count, total)
                self.timetable.sessions[index].preference_satisfcation_cost = p
            else:
                p = PreferenceSatisfacionCost(0, 0)

                self.timetable.sessions[index].preference_satisfcation_cost = p

    def evaluate_room_capacity(self):
        echo.print("Evaluating Room Capacity\n", color="green")
        for index, session in enumerate(self.timetable.sessions):
            total = session.group.total
            capacity = session.room.capacity

            self.timetable.sessions[index].room_capacity_cost = RoomCapacity(total, capacity)
