"""
The objective is to maximise the cost by all means

The cost rewards good behaviour and punishes the opposite
"""
from typing import List

from Objects.Internal.Priorities import Priorities


class Cost:
    def __init__(self, primary_value, secondary_value) -> None:
        self.primary_value = primary_value
        self.secondary_value = secondary_value
        self.value: int = 0
    
    @property
    def primary_value(self):
        return self._primary_value
    
    @primary_value.setter
    def primary_value(self, value):
        self._primary_value = value
  
    @property
    def secondary_value(self):
        return self._secondary_value
    
    @secondary_value.setter
    def secondary_value(self, value):
        self._secondary_value = value

    def __repr__(self):
        return f"Cost({self.primary_value}, {self.secondary_value})"
  
    def __str__(self):
        return f"(Cost:{self.primary_value}, {self.secondary_value} -> {self.value})"
  
    def __add__(self, other):
        if isinstance(other, Cost):
            
            self.value = (self.value + other.value) / 2
            return self
        elif isinstance(other, int):
            result = Cost(0, 0)
            result.value = self.value + other
            return result
  
 
    def __mul__(self, other):
        result = Cost(self.primary_value * other, self.secondary_value * other)
        result.value = self.value * other.value
        return result
  
    def __truediv__(self, other):
        result = Cost(self.primary_value / other, self.secondary_value / other)
        result.value = self.value / other.value
        return result
  
    def __floordiv__(self, other):
        result = Cost(self.primary_value // other, self.secondary_value // other)
        result.value = self.value // other.value
        return result
  
    def __mod__(self, other):
        result = Cost(self.primary_value % other, self.secondary_value % other)
        result.value = self.value % other.value
        return result
  
    def __pow__(self, other):
        result = Cost(self.primary_value ** other, self.secondary_value ** other)
        result.value = self.value ** other.value
        return result
  
    def __eq__(self, other):
        return (self.primary_value == other.primary_value) and (self.secondary_value == other.secondary_value) and (self.value == other.value)
  
    def __ne__(self, other):
        return (self.primary_value != other.primary_value) or (self.secondary_value != other.secondary_value) or (self.value != other.value)
  
    def __lt__(self, other):
        if self.primary_value < other.primary_value:
            return True
        elif self.primary_value == other.primary_value:
            if self.secondary_value < other.secondary_value:
                return True
            elif self.secondary_value == other.secondary_value:
                return self.value < other.value
        return False
  
    def __le__(self, other):
        if self.primary_value < other.primary_value:
            return True
        elif self.primary_value == other.primary_value:
            if self.secondary_value < other.secondary_value:
                return True
            elif self.secondary_value == other.secondary_value:
                return self.value <= other.value
        return False
  
    def __gt__(self, other):
        if isinstance(other, Cost):
            if self.value > other.value:
                return True
        elif isinstance(other, int):
            if self.value > other:
                return True
        return False
  
    def __ge__(self, other):
        if self.primary_value > other.primary_value:
            return True
        elif self.primary_value == other.primary_value:
            if self.secondary_value > other.secondary_value:
                return True
            elif self.secondary_value == other.secondary_value:
                return self.value >= other
    
class RoomCapacity(Cost):
    def __init__(self, group_size:int, siting_capacity:int) -> None: 
        super().__init__(group_size, siting_capacity)
        """
        This cost awards number of students sited

        """
        self.unseated = self.primary_value - self.secondary_value
        if self.unseated < 1:
            self.value = 100
        elif self.primary_value > self.secondary_value:
            self.value = 100 - (self.unseated / self.primary_value) * 100
        elif self.primary_value < self.secondary_value:
            self.value = 100

class ClashCost(Cost):
    def __init__(self, total_clashes:int) -> None: 
        super().__init__(1, total_clashes)
        """
        This cost awards least number of clashes
        That is Less complexity more cost
        """
        if self.secondary_value > 0:
            self.value = (self.primary_value/ self.secondary_value) * 100
        else:
            self.value = 100

class PreferenceSatisfacionCost(Cost):
    def __init__(self, satsified_preferences:int, total_preferences:int) -> None:
        super().__init__(satsified_preferences, total_preferences)
        self.preference_type: str
        self.calculate_value()
    
    def calculate_value(self):
        if self.primary_value == 0 and  self.secondary_value == 0:
            self.value =  100
        elif self.primary_value == 0 and self.secondary_value > 0:
            self.value = 0
        elif self.primary_value > 0 and self.secondary_value > 0:
            self.value = (self.primary_value / self.secondary_value) * 100

class PrioritySatisfaction(Cost):
    def __init__(self, priorities: Priorities) -> None:
        super().__init__(0, 0)
        self.cost_list = []
        self.total_cost: Cost
        self.priorities = priorities
        self.selected_priorities: List[int]
        self.priority_class: str
        self.preferences: List[PreferenceSatisfacionCost] = []

    def AddPreference(self, *preference: PreferenceSatisfacionCost):
        self.preferences.extend(preference)
    
    def calculate(self):
        for preference in self.preferences:
            if self.preferences[preference.preference_type] in self.selected_priorities:
                self.cost_list.append(preference)
        if len(self.cost_list) != 0:
            self.total_cost = sum(c for c in self.cost_list) / len(self.cost_list)
        else:
            c = Cost(0, 0)
            c.value =  100
            self.total_cost = c
   
class ClassOnePrioritySatisfaction(PrioritySatisfaction):
    def __init__(self, priorities: Priorities) -> None:
        super().__init__(priorities)
        self.priority_class = "one"
        self.selected_priorities = [1, 2]
        self.calculate()         
  
class ClassTwoPrioritySatisfaction(PrioritySatisfaction):
    def __init__(self, priorities: Priorities) -> None:
        super().__init__(priorities)
        self.priority_class = "two"
        self.selected_priorities = [3, 4]
        self.calculate()  

class Consecutive(Cost):
    def __init__(self, consecutive:bool=False) -> None:
        super().__init__(0, 0)
        self.consecutive = consecutive
        if consecutive:
            self.value = 100
        else:
            self.value = 0
        
class ConstraintSatisfaction(Cost):
    def __init__(self) -> None:
        super().__init__(0, 0)
        self.all_costs: List[Cost] = []

        self.total_cost: Cost = Cost(0, 0)
        self.complete_cost: int = 0

    
    def AddCost(self, *cost:Cost):
        self.all_costs.extend(cost)
        self.complete_cost += len(cost) * 100
        for c in cost:
            self.total_cost.value += c.value
        self.total_cost.value = (self.total_cost.value / self.complete_cost) * 100
    
    def __str__(self):
        return f'Complete Cost: {self.complete_cost} -> total_cost: {self.total_cost.value}'

class TotalConstraintCompliance(Cost):
    def __init__(self, hard_constraints: ConstraintSatisfaction, soft_constraints:ConstraintSatisfaction, soft_constraint_satisfaction_acceptance_rate: int) -> None:
        super().__init__(0, 0)
        self.soft_constraint_satisfaction_acceptance: int = soft_constraint_satisfaction_acceptance_rate

        self.value: int = (hard_constraints.total_cost.value + min(soft_constraints.total_cost.value+self.soft_constraint_satisfaction_acceptance, 100))/2

    @property
    def soft_constraint_satisfaction_acceptance(self):
        return self._soft_constraint_satisfaction_acceptance
    
    @soft_constraint_satisfaction_acceptance.setter
    def soft_constraint_satisfaction_acceptance(self, value:int):
        self._soft_constraint_satisfaction_acceptance = value