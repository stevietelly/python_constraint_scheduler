from Assets.Functions.Utilities import return_list_of_days, return_list_of_daytimes, return_list_of_times
from Logic.DateTime.Day import Day
from Logic.DateTime.Time import Time
from typing import List, Dict, Union
from Logic.DateTime.Week import Week
from Objects.Internal.Metadata import InputMetadata


class Configuration:
    """
    Data required to calibrate internal working of the program
    """
    def __init__(self, name:str, start_time: Time, end_time: Time, days: List[Day], system: dict, metadata) -> None:
        self.instiution_name: str = name
        self.start_time = start_time
        self.end_time = end_time
        self.metadata: InputMetadata = InputMetadata(metadata["input_version"], metadata["generator_type"], metadata["generator_version"])


        
        self.days = days
        self.week: Week = Week(self.days) 
        self.duration_per_session:int = system["duration_per_session"]
        self.total_duration_for_sessions: int = system["total_duration_for_sessions"]
        
        self.timelines: Dict[str, any] = {"times": None, "daytimes": None, "days": days}
        self._timelines()
        
    def _timelines(self):
        self.timelines["times"] = return_list_of_times(self.start_time, self.end_time, self.duration_per_session)
        self.timelines["daytimes"] = return_list_of_daytimes(self.days, self.timelines["times"])
      

    def __str__(self) -> str:
        return "<timetable configuration>"
    
    def __repr__(self) -> str:
        return "<timetable configuration>"