class Priorities:
    def __init__(self) -> None:
        """
        Priorities define whose preferences will be considered before the others
        """
        self.priorities: dict = {
            "room": 1,
            "instructors": 2,
            "units": 3,
            "groups": 4
        }
    
    def define(self, room:int, instructors:int, units:int, groups:int):
        self.priorities["room"] = room
        self.priorities["instructors"] = instructors
        self.priorities["units"] = units
        self.priorities["groups"] = groups
     
        # TODO: is courses priorities necessary?