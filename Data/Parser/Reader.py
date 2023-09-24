from typing import *
from Assets.Functions.Echo import Echo
from Assets.Functions.Utilities import return_list_of_days
from Data.Parser.BackwardsCompatibility.Reader import V_0_2_0
from Data.Parser.Preferences import PreferenceParser
from Logic.DateTime.Time import Time
from Logic.Structure.Configuration import Configuration
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group

from Objects.Physical.Rooms import Room

class DataReader:
    """
    This is the data Encoder,that converts the different
    attributes to python Code to be handled
            """
    def __init__(self, data: Dict) -> None:
        self.data = data

        self.configuration, self.units, self.instructors, self.programmes, self.rooms, self.groups = None, [], [], [], [], []

        if data["configuration"]["meta_data"]["input_version"] == "0.2.0":
            echo = Echo()
            echo.unmute(f"Input Version is 0.2.0 Defaulting to compatible version", color="magenta")
            reader = V_0_2_0(data)
            reader.Encode()
            self.configuration, self.units, self.instructors, self.programmes, self.rooms = reader.configuration, reader.units, reader.instructors, reader.programmes, reader.rooms
            print("version 0.2.0")
            exit()
    
    def Encode(self):
        """
        Convert to python Objects
        """
        self._encode_rooms()
        self._encode_units()
        self._encode_instructors()
        self._encode_configuration()
        self._encode_programmes()

    def Output(self)->dict:
        return {
        "configuration": self.configuration,
        "programmes": self.programmes,
        "instructors": self.instructors,
        "units": self.units,
        "rooms": self.rooms,
        "groups": self.groups
        }
    
    def _encode_rooms(self):
        for room in self.data["rooms"]:
            r = Room(room["id"], room["name"], room["capacity"], PreferenceParser(room["preferences"]).Parse())
            self.rooms.append(r)

    def _encode_units(self):
        for unit in self.data["units"]:
            u = Unit(unit["id"], unit["title"], unit["sessions"], unit["instructors"], PreferenceParser(unit["preferences"]).Parse())
            self.units.append(u)

    def _encode_instructors(self):
        for instructor in self.data["instructors"]:
            i =  Instructor(instructor["name"], instructor["title"], instructor["id"], PreferenceParser(instructor["preferences"]).Parse())
            self.instructors.append(i)
    
    def _encode_configuration(self):
        configuration = self.data["configuration"]
        start, end = Time(configuration["start_time"]), Time(configuration["end_time"])
        days = return_list_of_days(configuration["days"], start, end) 
        system = {"duration_per_session": configuration["duration"]["minimum"], "total_duration_for_sessions": configuration["duration"]["maximum"]}
        self.configuration = Configuration(configuration["name"], start, end, days, system)

    def _encode_programmes(self):
        for programme in self.data["programmes"]:
            p = Programme(programme["id"], programme["title"])
            
            groups = [Group(group["id"],group["title"], PreferenceParser(group["preferences"]).Parse(), units=group["units"])for group in programme["groups"]]
            self.groups.extend(groups)
            p.groups = groups
            self.programmes.append(p)
            