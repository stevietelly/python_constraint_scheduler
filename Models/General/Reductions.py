from copy import deepcopy
from Errors.Error import InvalidPreferenceFixing
from Errors.Exception import InvalidPreferenceClause, OverPreferencing
from Logic.Structure.Variables import Dynamic
from Objects.Internal.Preference.Preference import After, All, And, Before, Except, Only, Rule


class PreferencesReduction:
    """
    Reduce Values in a domain space that violate a preference
    """
    def __init__(self, preferences: Rule, dynamic_variable: Dynamic) -> None:
        self.preferences = preferences
        self.dynamic_variable = dynamic_variable
    
    def Reduce(self):
        self.lookup_maintainance(self.preferences)

    def lookup_maintainance(self, rule: Rule):
        if isinstance(rule, And):
            values = rule.values[0]
            for r in values:
                self.lookup_maintainance(r)
        elif isinstance(rule, All):
            pass
        else:
            if isinstance(rule, Except):
                self.except_rule_action(rule)
            elif isinstance(rule, Only):
                self.only_rule_action(rule)
            elif isinstance(rule, Before):
                self.before_rule_action(rule)
            elif isinstance(rule, After):
                self.after_rule_action(rule)
            else: print("done")
    
    def except_rule_action(self, rule: Rule):
        """For except rule clauses"""
        lookups = rule.value
        for lookup in lookups:
            match lookup.string_type_:
                case "time":
                    [[self.dynamic_variable.times.remove(t)] if t == lookup.value else None  for t in self.dynamic_variable.times]
                    if self.dynamic_variable.times == []: raise OverPreferencing(lookup, lookup.string_type_, "EXCEPT")
                case "day":
                    [[self.dynamic_variable.days.remove(d)] if d == lookup.value else None  for d in self.dynamic_variable.days]
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "EXCEPT")
                case "daytime":
                    [[self.dynamic_variable.daytimes.remove(dt)] if dt == lookup.value else None  for dt in self.dynamic_variable.daytimes]
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "EXCEPT")
                case "room":
                    print(lookup)
                    [[self.dynamic_variable.rooms.remove(r)] if r == lookup.value else None  for r in self.dynamic_variable.rooms]
                    if self.dynamic_variable.rooms == []: raise OverPreferencing(lookup, lookup.string_type_, "EXCEPT")
                case "instructor":
                    [[self.dynamic_variable.instructors.remove(i)] if i == lookup.value else None  for i in self.dynamic_variable.instructors]
                    if self.dynamic_variable.instructors == []: raise OverPreferencing(lookup, lookup.string_type_, "EXCEPT")
                case _:
                    InvalidPreferenceFixing("Unit", "EXCEPT")
    
    def only_rule_action(self, rule: Rule):
        """For only rule clauses"""
        lookups = rule.value
        for lookup in lookups:
            match lookup.string_type_:
                case "time":
                    [[self.dynamic_variable.times.remove(t)] if t != lookup.value else None  for t in self.dynamic_variable.times]
                    if self.dynamic_variable.times == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "day":
                    [[self.dynamic_variable.days.remove(d)] if d != lookup.value else None  for d in self.dynamic_variable.days]
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "daytime":
                    [[self.dynamic_variable.daytimes.remove(dt)] if dt != lookup.value else None  for dt in self.dynamic_variable.daytimes]
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "room":
                    print(lookup)
                    [[self.dynamic_variable.rooms.remove(r)] if r != lookup.value else None  for r in self.dynamic_variable.rooms]
                    if self.dynamic_variable.rooms == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "instructor":
                    [[self.dynamic_variable.instructors.remove(i)] if i != lookup.value else None  for i in self.dynamic_variable.instructors]
                    if self.dynamic_variable.instructors == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case _:
                    InvalidPreferenceFixing("Unit", "ONLY")
    
    def before_rule_action(self, rule: Rule):
        """For before rule clauses"""
        lookups = rule.value
        for lookup in lookups:
            match lookup.string_type_:
                case "time":
                    values = []
                    [values.append(t) if t <= lookup.value else None  for t in self.dynamic_variable.times]
                    self.dynamic_variable.times = values
                    if self.dynamic_variable.times == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "day":
                    values = []
                    [values.append(t) if t <= lookup.value else None  for t in self.dynamic_variable.days]
                    self.dynamic_variable.days = values
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "daytime":
                    values = []
                    [values.append(t) if t <= lookup.value else None  for t in self.dynamic_variable.daytimes]
                    self.dynamic_variable.daytimes = values
                    if self.dynamic_variable.daytimes == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "room":
                    raise InvalidPreferenceClause("room", "before")
                case "instructor":
                    raise InvalidPreferenceClause("instructor", "before")
                
    def after_rule_action(self, rule: Rule):
        """For after rule clauses"""
        lookups = rule.value
        for lookup in lookups:
            match lookup.string_type_:
                case "time":
                    values = []
                    [values.append(t) if t >= lookup.value else None  for t in self.dynamic_variable.times]
                    self.dynamic_variable.times = values
                    if self.dynamic_variable.times == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "day":
                    values = []
                    [values.append(t) if t >= lookup.value else None  for t in self.dynamic_variable.days]
                    self.dynamic_variable.days = values
                    if self.dynamic_variable.days == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "daytime":
                    values = []
                    [values.append(t) if t >= lookup.value else None  for t in self.dynamic_variable.daytimes]
                    self.dynamic_variable.daytimes = values
                    if self.dynamic_variable.daytimes == []: raise OverPreferencing(lookup, lookup.string_type_, "ONLY")
                case "room":
                    raise InvalidPreferenceClause("room", "before")
                case "instructor":
                    raise InvalidPreferenceClause("instructor", "before")
    
    