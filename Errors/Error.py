from Assets.Functions.Echo import Echo


class CustomError:
    def __init__(self, name:str, message: str) -> None:
        # Echo.state = True
        echo = Echo()
        
        echo.unmute(f"\n{name}: {message}", color="magenta")      

class InvalidPreferenceFixing(CustomError):
    def __init__(self, object_: any, clause: str) -> None:
        super().__init__(name="InvalidPreferenceFixing", message=f"Ignoring Invalid Preferences fixed in a '{object_}' at an '{clause}' clause, please read instructions on relevant clauses for each object.")
    
class MissingValueInPreference(CustomError):
    def __init__(self, object_: str, clause: str, value=None) -> None:
        super().__init__("MissingValueInPreference", message=f"Ignoring Preferences whose values is missing, fixed inside '{object_}' inside '{clause}', {value or 'Unknown'}")

class UnevaluatedTimetable(CustomError):
    def __init__(self) -> None:
        super().__init__("UnevaluatedTimetable", message="Send Through `FitnessEvaluation` Function")