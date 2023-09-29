from typing import Union
from Errors.Exception import *
from Logic.DateTime.Day import Day
from Objects.Internal.Preference.Preference import *
from Objects.Internal.Preference.Lookup import *



from Logic.DateTime.Time import Time
from Logic.DateTime.DayTime import DayTime
from Objects.Physical.Rooms import Room

class PreferenceParser:
    """
    Parses a string preference representation into a corresponding Rule object.

    Preference syntax:
    {QUALITY [TYPE:->'VALUE'] AND/OR [QUALITY [TYPE:->'VALUE'] AND/OR ...]}
    where
    - QUALITY: Before, After, Except, All, Only
    - TYPE: DAY, TIME, ROOM, DAYTIME, UNIT
    - VALUE: the value of the TYPE
    """

    def __init__(self, string: str):
        self.quality_mapping = {
            "before": Before,
            "after": After,
            "all": All,
            "only": Only,
            "except": Except,
            "and": And
        }
        self.rule_strings = ["before",
            "after",
            "all",
            "only",
            "except",
            "and"]
        self.value_mapping = {
     "time": LookupTime,
     "room": LookupRoom,
     "day": LookupDay,
     "daytime": LookupDayTime,
     "unit": LookupUnit,
     "group": LookupGroup,
     "instructor": LookupInstructor
 }
       
        self.string = string
        self.Parse()
    
    def Parse(self)-> Rule:
        return self.parser(self.string) if self.string is not None else All()

    def parser(self, text: str):
     
        if text.startswith("{"):
            text = text.replace("{", "")
            if "}" in text: text = text.replace("}", "")

            for mapping in self.quality_mapping:
                if mapping.upper() in text:
                    text = text.replace(mapping.upper(), "")
                    substring = self.parse_substring(text)
                    return self.quality_mapping[mapping](substring)  if type(substring) is not list else self.quality_mapping[mapping](*substring)
                elif  all([string.upper() in text for string in self.rule_strings]):
                    raise UnknownPreferenceSyntax(text)
                
            raise UnknownPreferenceSyntax(text)
        elif text.startswith("AND") and "{" in text:
            text = text.replace("AND ", "")
            new_strings = text.split("}, ")
            return And(*[self.parser(string) for string in new_strings])
        elif text == "ALL": return All()
        elif "{" and "}" not in text: raise InvalidPreferenceSyntax(message="missing `{}`", invalid_preference=text)
        
    def parse_substring(self, text:str):
        if "," in text:
            strings = text.split(",")
            return [self.parse_substring(string) for string in strings]
        else:
            for mapping in self.value_mapping:
                
                if "["+mapping.upper() +":->" in text:
                   
                    text = text.replace("[", '', 1)
                    text = text.replace("]", '', 1)
                    text = text.replace(f"{mapping.upper()}:->", "", 1)
                    text = text.replace("'", "", 2)
                    return self.value_mapping[mapping](text.strip())
                
        raise InvalidPreferenceSyntax(message="missing value", invalid_preference=text)
                
              
