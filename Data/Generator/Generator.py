import random
import string

from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write


class DataGenerator:
    

    def __init__(self, output_file:str):
        """
        A class to generate random data for the sake of testing
        """
        self.output_file = output_file
        self.output = {}
    
    def generateRandomPrefrence(self, objects: list|None = None):
        # TODO:Write the code to generate random preferences
        return None

    def GenerateInstructors(self, total:int):
        result = []
        for i in range(int(total)):
            result.append({"id": i+1, "preferences": self.generateRandomPrefrence()})
        self.output["instructors"] = result

    def GenerateUnits(self, total_units:int, total_instructors):
        result = []
        for i in range(int(total_units)):
            instructors = [i+1 for i in range(int(total_instructors))]
            result.append({"id": i+1, "preferences": self.generateRandomPrefrence(), "instructors": random.choices(instructors, k=random.randint(1, 3))})
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
            
   
    

    def GenerateAllInputData(self, instructors:int, groups:int, rooms:int, units:int, configuration):
        
        # self.output["configuration"] =  configuration["configuration"]
        self.GenerateInstructors(instructors)
        self.GenerateRooms(rooms)
        self.GenerateGroups(groups, units)
        self.GenerateUnits(units, instructors)

    def write(self):
        w = Write('', self.output_file, self.output)
        w.dump()


