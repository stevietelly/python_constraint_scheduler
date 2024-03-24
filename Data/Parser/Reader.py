from typing import Dict
from Assets.Functions.Echo import Echo
from Assets.Functions.Utilities import return_list_of_days
from Data.Parser.Preferences import PreferenceParser
from Errors.Exception import IncompatibleVersion
from Logic.DateTime.Time import Time
from Logic.Structure.Configuration import Configuration
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group

from Objects.Physical.Rooms import Room
echo = Echo()
class DataReader:
    """
    This is the data Encoder,that converts the different
    attributes to python Code to be handled
            """
    def __init__(self, data: Dict) -> None:
        self.data = data

        self.configuration, self.units, self.instructors, self.rooms, self.groups = None, [], [], [], []

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

    def Output(self)->dict:
        return {
        "configuration": self.configuration,
        "instructors": self.instructors,
        "units": self.units,
        "rooms": self.rooms,
        "groups": self.groups
        }
    
    def _encode_rooms(self):
        for room in self.data["rooms"]:
            r = Room(room["id"], room["capacity"], PreferenceParser(room["preferences"]).Parse())
            self.rooms.append(r)

    def _encode_units(self):
        for unit in self.data["units"]:
            u = Unit(unit["id"], unit["sessions"], unit["instructors"], PreferenceParser(unit["preferences"]).Parse())
            self.units.append(u)

    def _encode_instructors(self):
        for instructor in self.data["instructors"]:
            i =  Instructor(instructor["id"], PreferenceParser(instructor["preferences"]).Parse())
            self.instructors.append(i)
    
    def _encode_configuration(self):
        configuration = self.data["configuration"]
        start, end = Time(configuration["start_time"]), Time(configuration["end_time"])
        days = return_list_of_days(configuration["days"], start, end) 
        system = {"duration_per_session": configuration["duration"]["minimum"], "total_duration_for_sessions": configuration["duration"]["maximum"]}
        self.configuration = Configuration(configuration["name"], start, end, days, system, configuration["meta_data"])

    def _encode_groups(self):
        for group in self.data["groups"]:
            self.groups.append(Group(group["id"], group["total"], PreferenceParser(group["preferences"]).Parse(), group["units"]))
            
  