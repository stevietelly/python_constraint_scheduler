from Errors.Exception import InvalidPreferenceSyntax, UnknownPreferenceSyntax
from Objects.Internal.Preference.Lookup import LookupDay, LookupDayTime, LookupGroup, LookupInstructor, LookupRoom, LookupTime, LookupUnit
from Objects.Internal.Preference.Preference import After, All, And, Before, Except, Only, Rule

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
            "and": And,
        }
        self.rule_strings = ["before", "after", "all", "only", "except", "and"]
        self.value_mapping = {
            "time": LookupTime,
            "room": LookupRoom,
            "day": LookupDay,
            "daytime": LookupDayTime,
            "unit": LookupUnit,
            "group": LookupGroup,
            "instructor": LookupInstructor,
        }

        self.string = string
        self.Parse()

    def Parse(self) -> Rule:
        return self.parser(self.string) if self.string is not None else All()

    def parser(self, text: str):

        if text.startswith("{"):
            text = text.replace("{", "")
            if "}" in text:
                text = text.replace("}", "")

            for key, lookup in self.quality_mapping.items():
                if key.upper() in text:
                    text = text.replace(key.upper(), "")
                    substring = self.parse_substring(text)
                    return lookup(substring) if not isinstance(substring, list) else lookup(*substring)
            raise UnknownPreferenceSyntax(text)
        elif text.startswith("AND") and "{" in text:
            text = text.replace("AND ", "")
            new_strings = text.split("}, ")
            return And(*[self.parser(string) for string in new_strings])
        elif text == "ALL":
            return All()
        elif "{" and "}" not in text:
            raise InvalidPreferenceSyntax(
                message="missing `{}`", invalid_preference=text
            )

    def parse_substring(self, text: str):
        if "," in text:
            strings = text.split(",")
            return [self.parse_substring(string) for string in strings]
        else:
            for key, lookup in self.value_mapping.items():
                if "[" + key.upper() + ":->" in text:
                    text = text.replace("[", "", 1)
                    text = text.replace("]", "", 1)
                    text = text.replace(f"{key.upper()}:->", "", 1)
                    text = text.replace("'", "", 2)
                    return lookup(text.strip())
        raise InvalidPreferenceSyntax(message="missing value", invalid_preference=text)
