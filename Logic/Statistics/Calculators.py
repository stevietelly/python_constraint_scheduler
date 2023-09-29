from typing import List, Union, Dict
from Assets.Functions.Utilities import sort_sessions_by_daytime
from Logic.Compliance.Negative import CapacityInequality, Clash, ConsecutiveIncompliance, UnSatisfiedPreferences

from Logic.DateTime.Day import Day
from Logic.DateTime.Duration import Duration
from Logic.DateTime.Time import Time
from Objects.User.Preferences.Preference import Preferences
from Objects.User.Preferences.Rules import Before, After, All, Except, Only, And, Or, Rule
from Logic.Structure.Session import Session
from Logic.DateTime.DayTime import DayTime
from Objects.Persons.Instructor import Instructor
from Logic.Statistics.Costs.Cost import ClashCost, Consecutive, PreferenceSatisfacionCost, RoomCapacity, Cost

from Logic.Compliance.Positive import CapacityEquality, FreeGroupPeriod, FreeInstructorPeriod, FreePeriod, FreeRoomPeriod, SatisfiedPreferences

from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room


class Calculator:
    """
    The idea behind a calculator is to evaluate how good an object is in refrence to a temporal standpoint

    the following are created as a result
    -> Free Periods
    -> Clashing Periods
    -> Preferences Satisfaction (Costs)
    -> Consecutive Sessions
    :param tdfs -total duration for sessions
    """

    def __init__(self, object_: Union[Group, Room, Instructor] , daytimes: List[DayTime], days: List[Day], times: List[Time], maximum_consecutive_sessions: int):
        self.object_: Union[Group, Room, Instructor] = object_
        self.daytimes = daytimes
        self.days = days
        self.times = times
        self.maximum_consecutive_sessions: int = maximum_consecutive_sessions
     

        self.duration_per_session: int
        # TODO: do not forget to insert this value

        # Define object type
        self.object_type:str
        self.object_type = "room" if type(self.object_) == Room else "group"
        self.object_type = "instructor" if type(self.object_) == Instructor else "group"

        # A holder for all objecrs
        self.all_costs: Dict[str, List[Cost]] = {
            "preferences": [],
            "clashes": [],
            "consecutiveness": []
        }

        self.identifier: int = self.object_.identifier
        self.preferences_cost: List[PreferenceSatisfacionCost] = []

        # sed for clash analysis
        self.clash_holder: Dict[DayTime, List[Session]] = {}

        # hosl all sessions
        self.all_sessions: List[Session] = []

        # Compliances
        # Positive
        self.satisfied_preferences = SatisfiedPreferences()
        # TODO: This does not make sense, the one above ^
        self.clashes: Dict[str, List[Clash]] = {
            "room": [],
            "group": [],
            "instructor": []
        }


        # Negative
        self.unsatisfied_preferences = UnSatisfiedPreferences()
        self.free_periods: List[FreePeriod] = []
        self.single_free_period: FreePeriod = FreePeriod(self.object_, DayTime(Day("monday", None, None), Time("0:00am")))
        self.consecutiveIncompliance = ConsecutiveIncompliance()

        self.object_session_holder: Dict[Union[Group, Room, Instructor], List[Session]] = {

        }
       
        self.Divide()

    def Divide(self):
        for daytime in self.daytimes:
            self.clash_holder[daytime] = []
      
    def AddSession(self, session: Session):
        if session.resources[self.object_type].identifier == self.identifier:
            self.clash_holder[session.daytime].append(session)
            object_ = self.get_session_object(session, self.object_)
            if object_ not in self.object_session_holder:
                self.object_session_holder[object_] = []

            self.object_session_holder[object_].append(session)

            self.all_sessions.append(session)
       
    def Calculate(self):
        # Clash
        self.ClashCheck()
        # Preferences
        self.PreferenceCompliance()
        # Consecutiveness
        self.ConsecutiveCheck()    

    def RuleCheck(self, rule: Rule, session: Session) -> bool:
        #  get th list of the required objects_
        list_ = self.daytimes if type(rule.value) == DayTime else self.times
        list_ = self.days if type(rule.value) == Day else self.times

        object_ = self.get_session_object(session, rule.value)
        if type(rule) == Before:
            
            # get the range for compliance
            all_items = get_data_list(list_, 0, rule.value, "before") 
            if object_ in all_items:
                return True
        elif type(rule) == After:
        
            # get the range for compliance
            all_items = get_data_list(list_, 0, rule.value, "after")
            if object_ in all_items:
                return True
        elif type(rule) ==  All:
            return True
        elif type(rule) ==  Only:
            rule.value: List
            if object_ in rule.value:
                return True
        elif type(rule.value) == Except:
            if object_ != rule.value:
                return True
        elif type(rule.value) == And:
            primary_rule: Rule = self.RuleCheck(rule.primary)
            secondary_rule: Rule = self.RuleCheck(rule.secondary)

            if primary_rule and secondary_rule:
                return True
        elif type(rule) ==  Or:
            primary_rule: Rule = self.RuleCheck(rule.primary)
            secondary_rule: Rule = self.RuleCheck(rule.secondary)

            if primary_rule or secondary_rule:
                return True
        return False
                
    def PreferenceCompliance(self):
        for session in self.all_sessions:
            satisfied_rules = 0
            cost: PreferenceSatisfacionCost
            for rule in self.object_.preferences.rules:
                if self.RuleCheck(rule, session):
                    self.satisfied_preferences.AddSession(session)
                    satisfied_rules += 1
                else:
                    self.unsatisfied_preferences.AddSession(session)
            cost =  PreferenceSatisfacionCost(satisfied_rules, len(self.object_.preferences.rules))
            cost.preference_type = self.object_type

            new_session = session
            new_session.preference_compliance_cost[self.object_type] = cost
            self.ReplaceSession(session, new_session)
  
    def get_session_object(self, session: Session, object_type: Union[Time, Room, Instructor, DayTime, Day]) -> Union[Time, Room, Instructor, DayTime, Day]:
        return_type =  session.room if type(object_type) == Room else session.schedule.instructor
        return_type =  session.schedule.daytime if type(object_type) == DayTime else session.schedule.instructor
        return_type =  session.day if type(object_type) == Day else session.schedule.instructor
        return_type =  session.schedule.daytime.time if type(object_type) == Time else session.schedule.instructor
        return return_type
           
    def ClashCheck(self):
        free_period_keys = []
        for key, value in self.clash_holder.items():
            total = len(value)
            c = Clash(self.object_, key)
            if total > 1:
                """Calculate Cost"""
                cost = ClashCost(total)
               
         
                for session in value:
                    calculated_session = self.FindSession(session.identifier)
                    calculated_session.clash_costs[self.object_type] = cost
                    self.ReplaceSession(session, calculated_session)
                    c.AddSession(calculated_session)

                self.clashes[self.object_type].append(c)

            elif total <= 1:
                cost = ClashCost(total)
                for session in value:
                    calculated_session = self.FindSession(session.identifier)
                    calculated_session.clash_costs[self.object_] = cost
                    self.ReplaceSession(session, calculated_session)
                    
       

                if key not in free_period_keys:
                    free_period_keys.append(key)

        for key in free_period_keys:
            self.single_free_period.daytime = key      
            self.free_periods.append(self.single_free_period)
              
    def ConsecutiveCheck(self):
        # FIXME: Consecutive calcuations
        for _, sessions in self.object_session_holder.items():
            sessions = sort_sessions(sessions)
            consecutive_sessions = self.find_consecutive_sessions(sessions)
            self.consecutiveIncompliance.AddSession(consecutive_sessions)

    def find_consecutive_sessions(self, sessions: List[Session]):
        """
        Finds consecutive sessions in a given object that span up to a limit of 'limit' number of sessions

        :param sessions: A list of Session objects to check for consecutive sessions

        :return: A list of lists containing consecutive sessions, where each sublist contains at least two sessions
        """
      
        consecutive_sessions: List[Session] = []
        # Sessions come sorted
        for i, session in enumerate(sessions):
            
           
            j = i + 1
            consecutive_count = 1
            consecutive_list = []
            
            while j < len(sessions) and consecutive_count < self.maximum_consecutive_sessions:
                next_session = sessions[j]
                
                if next_session.day == session.day and next_session.time == session.time + Duration(self.duration_per_session, 0):
                    consecutive_count += 1
                    consecutive_list.append(next_session)
                else:
                    break
                j += 1

      
       
            if consecutive_count >= self.maximum_consecutive_sessions:
                consecutive_sessions.append(consecutive_list)
   
        if consecutive_sessions:
         
    
            for sessions in consecutive_sessions:
                for session in sessions:
                    new_session = session
                    new_session.consecutive_cost[self.object_type] = Consecutive(True)
                    self.ReplaceSession(session, new_session)
                    self.all_costs["preferences"].append(Consecutive(True))
        return consecutive_sessions
        
    def FindSession(self, session_identifier: int) -> Session:
        """
        Find a specific Session given the sesssion id
        """
        for session in self.all_sessions:
            if session.identifier == session_identifier:
                return session
    
    def ReplaceSession(self, old_session: Session, new_session: Session):
        """
        This is to change a session from a previous state into a new updated one
        old session->new session
        """
        index = self.all_sessions.index(old_session)
        self.all_sessions[index] = new_session

    @staticmethod
    def ExtractIdentifiers(sessions: list):
        identifiers = []
        for session in sessions:
            identifiers.append(session.schedule.identifier)
        del sessions
        return identifiers

class RoomCalculator(Calculator):
    def __init__(self, room: Room, daytimes: List[DayTime], days: List[Day], times: List[Time], maximum_consecutive_sessions: int):
        super().__init__(room, daytimes, days, times, maximum_consecutive_sessions=maximum_consecutive_sessions)
        self.capacity_inequality = CapacityInequality(self.object_)
        self.capacity_equality: CapacityEquality = CapacityEquality(self.object_)
        self.object_type = "room"
        self.capacity_costs: List[RoomCapacity] = []


        # Consecutive calculations
        self.room_session_holder: Dict[Room, List[Session]] = {}

        self.free_periods: List[FreeRoomPeriod] = []
        self.single_free_period: FreeRoomPeriod = FreeRoomPeriod(self.object_, DayTime(Day("monday", None, None), Time("0:00am")))
    




    def Calculate(self):
        super().Calculate()
        for session in self.all_sessions:
            c = RoomCapacity(session.schedule.group.total, self.object_.capacity)
            session.room_capacity_cost = c
            if self.object_.capacity < session.schedule.group.total:
    
                self.capacity_inequality.AddSession(session)
            else:
                self.capacity_equality.AddSession(session)
            self.capacity_costs.append(c)

class GroupCalculator(Calculator):
    def __init__(self, group: Group, daytimes: List[DayTime], days: List[Day], times: List[Time], maximum_consecutive_sessions: int):
        super().__init__(group, daytimes, days,times, maximum_consecutive_sessions)
       
        self.object_type = "group"
        self.free_periods: List[FreeGroupPeriod] = []
        self.single_free_period = FreeGroupPeriod(self.object_, DayTime(Day("monday", None, None), Time("0:00am")))

class InstructorCalculator(Calculator):
    def __init__(self, instructor: Instructor, daytimes: List[DayTime], days: List[Day], times: List[Time], maximum_consecutive_sessions: int):
        super().__init__(instructor, daytimes, days,times, maximum_consecutive_sessions)
       
        self.object_type = "instructor"
        self.free_periods: List[FreeInstructorPeriod] = []
        self.single_free_period = FreeInstructorPeriod(self.object_, DayTime(Day("monday", None, None), Time("0:00am")))


    
    