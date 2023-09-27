
from Assets.Functions.Echo import Echo


class CustomException:
    """
    The base class Exception for the program that completetly
    exits when an issue is encountered to prevent the program from breaking
    """
    def __init__(self, message: str, string="") -> None:
        self.string = string
     
        self.message = message

        Echo().exit(f"{self.string}: {self.message}")
        exit()

class MissingClassList(CustomException):
    def __init__(self) -> None:
        super().__init__("Per instructions please input a list of str inside Day.days", "Missing Class List")


class InvalidPreferenceSyntax(CustomException):
    def __init__(self, message: str, invalid_preference: str) -> None:
        super().__init__(message + " in "+ f"'{invalid_preference}'", string="Invalid Preference Syntax")

class UnknownPreferenceSyntax(CustomException):
    def __init__(self, message: str) -> None:
        super().__init__(message, "Unknown Preference Syntax")

class InvalidTime(CustomException):
    def __init__(self, time) -> None:
        super().__init__(time, "Invalid Time")

class OverPreferencing(CustomException):
    def __init__(self, position, type_, clause: str) -> None:
        super().__init__(f"Leading to empty values, please limit your preferences at {position} inside {type_} at clause {clause}", "OverPreferencing")

class InvalidPreferenceClause(CustomException):
    def __init__(self, type_:str, clause:str) -> None:
        super().__init__(f"Cannot have a {type_} inside clause '{clause.upper()}'", string="InvalidPreferenceClause")

class SimilarObjectToPreference(CustomException):
    def __init__(self, lookup_str, type_) -> None:
        super().__init__(string="SimilarObjectToPreference", message=f"Similar Object '{type_}' to placed preference {lookup_str}")

class NoValueFound(CustomException):
    def __init__(self, static_variable, value="value") -> None:
        super().__init__(message=f"Exhausted all {value} for {static_variable}", string="NoValueFound")

class NoAssignmenetPossible(CustomException):
    def __init__(self, message: str, string="") -> None:
        super().__init__(message, string)