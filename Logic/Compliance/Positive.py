from typing import Union
from Logic.Compliance.Compliance import Compliance
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from Logic.DateTime.DayTime import DayTime


class PositiveCompliance(Compliance):
    def __init__(self) -> None:
        super().__init__()
        self.compliance_type = "positive"

class AcceptedCapacity(PositiveCompliance):
    def __init__(self, object_: Room) -> None:
        super().__init__()
        self.room: Room = object_

class FreePeriod(PositiveCompliance):
    def __init__(self, object_: Union[Group, Room, Instructor], daytime: DayTime) -> None:
        """
        A daytime in which a certain object has no session in
        """
        super().__init__()
        self.daytime: DayTime = daytime
        self.object_: Union[Group, Room, Instructor] = object_

class FreeGroupPeriod(FreePeriod):
    def __init__(self, group: Group, daytime: DayTime) -> None:
        """
        A specific daytime when a group  has no sessions
        """
        super().__init__(group, daytime)

class FreeRoomPeriod(FreePeriod):
    def __init__(self, room: Room, daytime: DayTime) -> None:
        """
        A specific daytime when a room  has no sessions
        """
        super().__init__(room, daytime)

class FreeInstructorPeriod(FreePeriod):
    def __init__(self, instructor: Instructor, daytime: DayTime) -> None:
        """
        A specific daytime when an instructor  has no sessions
        """
        super().__init__(instructor, daytime)
    


class SatisfiedPreferences(PositiveCompliance):
    def __init__(self) -> None:
        super().__init__()

class CapacityEquality(PositiveCompliance):
    def __init__(self, room: Room) -> None:
        super().__init__()
