from typing  import Dict, List
from Assets.Functions.Echo import Echo
from Assets.Functions.Utilities import return_list_of_days, return_list_of_times
from Data.Parser.Preferences import PreferenceParser
from Errors.Exception import IncompatibleVersion
from Logic.DateTime.Day import Day
from Logic.DateTime.Time import Time
from Logic.Structure.Configuration import Configuration
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group

from Objects.Physical.Rooms import Room
echo = Echo()

class ReaderOutput:
    """
    ReaderOuput
    """
    def __init__(self) -> None:
        self.configuration: Configuration
        self.units, self.instructors, self.rooms, self.groups = [], [], [], []
        self.times = []
        self.days = []

    def is_filled(self) -> bool:
        return all([self.configuration is not None, len(self.rooms) > 1, len(self.units) > 1, len(self.instructors) > 1, len(self.groups) > 1])

    def __str__(self) -> str:
        return f"ReaderOutput: {'filled' if self.is_filled() else 'empty'}"

class DataReader:
    """
    This is the data Encoder,that converts the different
    attributes to python Code to be handled
            """
    def __init__(self, data: Dict) -> None:
        self.data = data
        self.configuration: Configuration = None
        self.units: List[Unit] = []
        self.instructors: List[Instructor] = []
        self.rooms: List[Room] = []
        self.groups: List[Group] = []
        self.days: List[Day] = []
        self.times: List[Time] = []
        if not data["configuration"]["meta_data"]["input_version"] == "0.4.0": raise IncompatibleVersion("0.4.0", data["configuration"]["meta_data"]["input_version"], "Input") 
        echo.print("\nEnoding Discovered Objects", color="magenta")

    def Encode(self):
        """
        Convert to python Objects
        """
       
        echo.print("Reading Rooms", color="green")
        self._encode_rooms()
        echo.print("Reading Units", color="green")

        self._encode_units()
        echo.print("Reading Instructors", color="green")

        self._encode_instructors()
        echo.print("Reading Configuration", color="green")

        self._encode_configuration()
        echo.print("Reading Groups", color="green")

        self._encode_groups()

    def Output(self)->ReaderOutput:
        r = ReaderOutput()
        r.groups = self.groups
        r.instructors = self.instructors
        r.configuration = self.configuration
        r.units = self.units
        r.rooms = self.rooms
        r.days, r.times = self.days, self.times
        return r

    def _encode_rooms(self):
        for room in self.data["rooms"]:
            r = Room(room["id"], room["capacity"], PreferenceParser(room["preferences"]).Parse())
            self.rooms.append(r)

    def _encode_units(self):
        for unit in self.data["units"]:
            u = Unit(unit["id"], unit["lessons"], unit["instructors"], PreferenceParser(unit["preferences"]).Parse())
            self.units.append(u)

    def _encode_instructors(self):
        for instructor in self.data["instructors"]:
            i =  Instructor(instructor["id"], PreferenceParser(instructor["preferences"]).Parse())
            self.instructors.append(i)
    
    def _encode_configuration(self):
        configuration = self.data["configuration"]
        start, end = Time(configuration["start_time"]), Time(configuration["end_time"])
        days = return_list_of_days(configuration["days"], start, end) 
        times = return_list_of_times(start, end, configuration["duration"]["minimum"])
        self.times =  times
        self.days =  days
        system = {"duration_per_session": configuration["duration"]["minimum"], "total_duration_for_sessions": configuration["duration"]["maximum"]}
        self.configuration = Configuration(configuration["name"], start, end, days, system, configuration["meta_data"])

    def _encode_groups(self):
        for group in self.data["groups"]:
            self.groups.append(Group(group["id"], group["total"], PreferenceParser(group["preferences"]).Parse(), group["units"]))
            
  