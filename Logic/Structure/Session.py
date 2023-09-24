from Logic.Structure.Variables import Dynamic, Static


class Session:
    def __init__(self, static_variable: Static, dynamic_variable: Dynamic = None) -> None:
        self.static_variable: Static = static_variable
        self.dynamic_variable: Dynamic = dynamic_variable
    
    def serialize(self)->dict:
        return {
            "group": self.static_variable.group.identifier,
            "unit": self.static_variable.unit.identifier,
            "time": str(self.dynamic_variable.time),
            "day": str(self.dynamic_variable.Day),
            # "instructor": self.dynamic_variable.instructor.identifier,
            "room": self.dynamic_variable.room.identifier
            }
    