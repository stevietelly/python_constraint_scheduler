from typing import *
from Assets.Functions.Utilities import return_list_of_days
from Data.Parser.Preferences import PreferenceParser
from Logic.DateTime.Time import Time
from Logic.Structure.Configuration import Configuration
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group

from Objects.Physical.Rooms import Room

class V_0_2_0:
    """
    This is the data Encoder,that converts the different
    attributes to python Code to be handled
            """
    def __init__(self, data: Dict) -> None:
        self.data = data

        self.configuration, self.units, self.instructors, self.programmes, self.rooms = None, [], [], [], []
        
    
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
        "rooms": self.rooms
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
          
            p = Programme(programme["id"], programme["title"], programme["levels"]["total"])
            p.groups = [[Group(group["id"], group["total"], PreferenceParser(group["preferences"]).Parse()) for group in level ]for level in programme["levels"]["groups"]]
            p.units = programme["levels"]["units"]
            self.programmes.append(p)