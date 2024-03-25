import random
from Assets.FileHandling.Write import Write
from Assets.Functions.Utilities import generate_days


class DataGenerator:
    """
    Data Generator
    Generating data for testing the different models 
    """
    def __init__(self, output_file:str = "output.json"):
        """
        A class to generate random data for the sake of testing
        """
        self.output_file = output_file
        self.output = {}

    def generateRandomPrefrence(self, objects: list|None = None):
        # TODO:Write the code to generate random preferences
        return objects

    def GenerateInstructors(self, total:int):
        result = []
        for i in range(int(total)):
            result.append({"id": i+1, "preferences": self.generateRandomPrefrence()})
        self.output["instructors"] = result

    def GenerateUnits(self, total_units:int, total_instructors: int):
        result = []
        for i in range(int(total_units)):
            instructors = [i+1 for i in range(int(total_instructors))]
            result.append({"id": i+1, "preferences": self.generateRandomPrefrence(),"sessions": random.randint(1, 3), "instructors": random.choices(instructors, k=random.randint(1, 3))})
        self.output["units"] = result

    def GenerateRooms(self, total):
        total = int(total)
        result = []
        for i in range(total):
            capacity = random.randint(20, 100)
            
            temp = {
                "id": i + 1,
             
                "capacity": capacity,
                "preferences": self.generateRandomPrefrence()
            }
            result.append(temp)
        self.output["rooms"] = result

    def GenerateGroups(self, total_groups, total_units):
        total = int(total_groups)
        result = []
        for i in range(total):
            total = random.randint(20, 100)
            units = random.choices([i+1 for i in range(total_units)], k=random.randint(1, 3))
            temp = {
                "id": i + 1,
                "units": units,
                "total": total,
                "preferences": self.generateRandomPrefrence()
            }
            result.append(temp)
        self.output["groups"] = result

    def GenerateConfiguration(self, name: str, num_days: int, start_day: str, start_time:str, end_time:str, duration_per_session: int):
        days = generate_days(start_day, num_days)

        config_list = {
            "name": name,
            "days": days,
            "start_day": start_day,
            "start_time": start_time,
            "end_time": end_time,
            "duration-per-session": duration_per_session,
            "priorities": {"room": None, "instructors": None, "units": None, "groups": None},
            "meta_data": {"input_version": "0.4.0", "generator_type": "manual","generator_version": "0.2.0"},
            "duration": {"maximum": 3, "minimum": 1, "division": "hour"},
            "constraint_satisfaction": {"soft": None, "hard": None},
            "consecutive": {"room": None, "instructor": None, "group": None},
            "system": {"limit": 0, "saturation": True, "tries": 0}
        }
        self.output["configuration"] = config_list

    def GenerateAllInputData(self, instructors:int, groups:int, rooms:int, units:int, config: None|dict =None):

        if config is None:self.GenerateConfiguration("", 5, "Monday", "8am", "4pm", 1) # default configuration settings
        else: self.output["configuration"] = config
        self.GenerateInstructors(instructors)
        self.GenerateRooms(rooms)
        self.GenerateGroups(groups, units)
        self.GenerateUnits(units, instructors)

    def write(self):
        w = Write('', self.output_file, self.output)
        w.dump()
