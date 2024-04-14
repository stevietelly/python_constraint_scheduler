from typing import List

from prettytable import PrettyTable
from Assets.Functions.Echo import Echo
from Data.Parser.Reader import ReaderOutput
from Errors.Error import UnevaluatedTimetable
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Logic.Statistics.Costs.Cost import ClashCost


from Logic.Structure.Session import Session

echo = Echo()


class Timetable:
    """
    This is a Timetable Class, with several methods to better manage it
    """

    def __init__(self, sessions: List[Session]) -> None:

        self.sessions = sessions
        self.free_periods: dict = {}.fromkeys(["rooms", "instructors", "groups"], [])
        self.clashes: dict = {}.fromkeys(["rooms", "instructors", "groups"], [])
        self.evaluated = False
        self.Statistics()

    def GetAllSessionByGroup(self, group_identifier: int):
        sessions = []
        for session in self.sessions:
            if session.group.identifier == group_identifier:
                sessions.append(session)
        return sessions

    def GetAllSessionByRoom(self, room_identifier: int):
        sessions = []
        for session in self.sessions:
            if session.room.identifier == room_identifier:
                sessions.append(session)
        return sessions

    def GetAllSessionByInstructor(self, instructor_identifier: int):
        sessions = []
        for session in self.sessions:
            if session.instructor.identifier == instructor_identifier:
                sessions.append(session)
        return sessions

    def SetPreferenceSatisfactionCost(self, identifier: int, p):
        for index, session in enumerate(self.sessions):
            if session.identifier == identifier:
                self.sessions[index] = p

    def GetIndexOfSession(self, session_identifier: int):
        for session in self.sessions:
            if session.identifier == session_identifier:
                return self.sessions.index(session)

    def GetSessionClashCost(self, session: Session):
        index = self.GetIndexOfSession(session.identifier)
        for group_clashes in self.clashes["groups"]:
            if session.group.identifier == group_clashes.object_.identifier:
                total = len(group_clashes.sessions_holder)
                c = ClashCost(total)
                self.sessions[index].AddClashCost(c)
        for instructor_clashes in self.clashes["instructors"]:
            if session.group.identifier == instructor_clashes.object_.identifier:
                total = len(instructor_clashes.sessions_holder)
                ic = ClashCost(total)
                self.sessions[index].AddClashCost(ic)
        for room_clashes in self.clashes["rooms"]:
            if session.group.identifier == room_clashes.object_.identifier:
                total = len(room_clashes.sessions_holder)
                rc = ClashCost(total)
                self.sessions[index].AddClashCost(rc)

    def GetSessionsByDayTime(self, daytime: DayTime):
        result = list()
        for session in self.sessions:
            if session.daytime == daytime:
                result.append(session)
        return result

    def GetSessionsByDayAndTime(self, day: Day, time: Time):
        daytime = DayTime(day, time)
        return self.GetSessionsByDayTime(daytime)

    def Output(self):
        clashes = {
            type_: [
                {
                    "identifier": clash.object_.identifier,
                    "sessions": clash.sessions_holder,
                }
                for clash in clashes
            ]
            for type_, clashes in self.clashes.items()
        }
        sessions = []
        for session in self.sessions:
            self.GetSessionClashCost(session)
            sessions.append(session.serialize())
        return {"clashes": clashes, "sessions": sessions}

    def Statistics(self):
        clash_cost = None
        preference_cost = None
        room_cost = None
        for session in self.sessions:
            if clash_cost is None:
                clash_cost = session.clash_cost
            elif clash_cost is not None:
                clash_cost += session.clash_cost

            if preference_cost is None:
                preference_cost = session.preference_satisfcation_cost
            elif preference_cost is not None:
                preference_cost += session.preference_satisfcation_cost

            if room_cost is None:
                room_cost = session.room_capacity_cost
            elif room_cost is not None:
                room_cost += session.room_capacity_cost
        self.clash_cost = clash_cost


class PrintTimetable:
    """
    A class that allows a Timetable to be printed to the terminal
    """

    def __init__(self, timetable: Timetable, reader_output: ReaderOutput) -> None:
        self.timetable = timetable
        self.reader_output = reader_output
        self.days = reader_output.configuration.days
        self.times = reader_output.configuration.timelines["times"]
        if not self.timetable.evaluated:
            UnevaluatedTimetable()

    def add_session(self, day, time):
        result = ""
        count = 0
        for session in self.timetable.sessions:
            if session.daytime.day == day and session.daytime.time == time:
                if count != 0:
                    result += "\n"
                result += f"{session.identifier} Group:{session.group.identifier} Unit:{session.unit.identifier} Instructor:{session.instructor.identifier} Room:{session.room.identifier}"
                count += 1

        return (
            result  # Return empty string if no session found for the given parameters
        )

    def print_stats(self):
        no_of_clashes = (
            len(self.timetable.clashes["rooms"])
            + len(self.timetable.clashes["instructors"])
            + len(self.timetable.clashes["groups"])
        )
        echo.unmute("\nFinal Timetable: ", color="cyan")
        echo.unmute(f"{no_of_clashes} total Clashes")
        echo.unmute(f"{len(self.timetable.clashes['rooms'])} clashes involving rooms")
        echo.unmute(
            f"{len(self.timetable.clashes['instructors'])} clashes involving instructors"
        )
        echo.unmute(f"{len(self.timetable.clashes['groups'])} clashes involving groups")

    def Print(self):
        self.print_stats()
        rows = ["Time"]
        rows.extend([str(d) for d in self.days])

        # Initialize a table with column names
        table = PrettyTable(rows)
        # Populate the timetable
        for time in self.times:
            row_data = [time]
            for day in self.days:
                sessions_info = self.add_session(day, time)

                if sessions_info != "":
                    row_data.append(sessions_info)
                else:
                    row_data.append(None)

            table.add_row(row_data, divider=True)

        print(table)
