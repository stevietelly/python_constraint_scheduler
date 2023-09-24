from typing import Any, Dict
from Errors.Error import *
from Errors.Exception import *
from Models.ConstraintSatisfaction.Domain import Domain
from Objects.User.Preference.Preference import *


class NodeConsistency:
    def __init__(self, reader_output:Dict[str, Any], variables ,resources, type_) -> None:
        self.reader_output = reader_output
        self.timelines = self.reader_output["configuration"].timelines
        self.type_ = type_
       
        self.domain: Domain = Domain(variables, resources)
        self.variables = variables
        
    def Consistency(self):
        for variable in self.variables:
            preferences = variable.preferences
            values = self.domain.get_value(variable).copy()
            final_value, change = self.lookup_value_maintainance(preferences, values)
            
           
            if change: self.domain.set_value(variable, final_value)
       
        
    def lookup_value_maintainance(self, rule: Rule, value: Dict[str, any]):
        new_value = value.copy()
        change = False
       
        if isinstance(rule, And):
            rule: And =  rule
            value = value
            for r in rule.values[0]:
                value, change = self.lookup_value_maintainance(r, value)
            return value, change

        else:
            if isinstance(rule, Except):
                change = True
                value = self.except_rule_action(rule, new_value)
                
            elif isinstance(rule, Only):
               change =  True
               value =  self.only_rule_action(rule, new_value)
            elif isinstance(rule, Before):
                change =  True
                value =  self.before_rule_action(rule, new_value)
            elif isinstance(rule, After):
                change =  True
                value =  self.after_rule_action(rule, new_value)
            elif isinstance(rule, All): pass
            else: raise UnknownPreferenceSyntax(str(rule))
        return new_value, change
                                 
    def only_rule_action(self, rule: Rule, values):
        type_ =  self.type_
        lookups = rule.value
       
        value_copies = values.copy()
        for lookup in lookups:
            self.on_similar_type(lookup.string_type_, type_)
            match lookup.string_type_:
                case "time": 
                    singular_values: list = values['daytime']
                    if not all([s.time != lookup.value for s in singular_values]):

                        values['daytime'] = [daytime for daytime in singular_values if daytime.time == lookup.value]
                    else:

                        values["daytime"].extend([daytime for daytime in value_copies if daytime.time == lookup.value])

                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "only")
                case "daytime":
                    singular_values: list = values['daytime']
                    if not all([s != lookup.value for s in singular_values]):
                    
                        values['daytime'] = [daytime for daytime in singular_values if daytime == lookup.value]
                    else:
                        values['daytime'].extend([daytime for daytime in value_copies if daytime == lookup.value])

                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "only")

                case "day":
                    # FIXME: 
                    singular_values: list = values['daytime']
                    if not all([s.day != lookup.value for s in singular_values]):
                        
                        values['daytime'] = [daytime for daytime in singular_values if daytime.day == lookup.value]
                       
                    else:
                        values["daytime"].extend([daytime for daytime in value_copies["daytime"] if daytime.day == lookup.value])
                     

                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "only")

                case "room":
                    singular_values: list = values['room']
                    if not all([s.identifier != int(lookup.value) for s in singular_values]):
                        values['room'] = [room for room in singular_values if room.identifier == int(lookup.value)]
                    else:
                        values['room'].extend([room for room in value_copies["room"] if room.identifier == int(lookup.value)])
                    if values['room'] == []: raise OverPreferencing(lookup, type_, "only")
                case "instructor":
                    singular_values: list = values["instructor"]
                    if not all([s.identifier != lookup.value for s in singular_values]):
                        values["instructor"] = [instructor for instructor in singular_values if instructor.identifier == lookup.value ]
                    else:
                        values["instructor"].extend([instructor for instructor in value_copies["instructor"] if instructor.identifier == lookup.value ])
                    if values['instructor'] == []: raise OverPreferencing(lookup, type_, "only")
 

    def after_rule_action(self, rule: Rule, values):
        type_=self.type_
        lookups = rule.value
        for lookup in lookups:
            self.on_similar_type(lookup.string_type_, type_)
            match lookup.string_type_:
                case "time": 
                    times = self.timelines["times"]
                    relevant = [time for time in times if time > lookup.value]
                    values["daytime"] = [daytime for daytime in values["daytime"] if daytime.time in relevant]
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "after")
                case "daytime":
                #    TODO: Daytime After
                    daytimes = self.timelines["daytimes"]
                    relevant = [daytime for daytime in daytimes if daytime > lookup.value]
                    values["daytime"] = relevant

                    
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "after")

                case "day":
                #    TODO: Day After
                    days = self.timelines["days"]
                    relevant = [day for day in days if day > lookup.value]
                    values["daytime"] = relevant

        
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "after")

                case "room":
                    raise InvalidPreferenceClause("room", "after")
                case "instructor":
                    raise InvalidPreferenceClause("instructoe", "before")

    def before_rule_action(self, rule: Rule, values):
        type_ = self.type_
        lookups = rule.value
        for lookup in lookups:
            self.on_similar_type(lookup.string_type_, type_)
            match lookup.string_type_:
                case "time": 
                    times = self.timelines["times"]
                    relevant = [time for time in times if time > lookup.value]
                    values["daytime"] = [daytime for daytime in values["daytime"] if daytime.time in relevant]
                  
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "before")
                case "daytime":
                #    TODO: Daytime After
                    daytimes = self.timelines["daytimes"]
                    
                    relevant = [daytime for daytime in daytimes if daytime > lookup.value]
                    
                    
                    values["daytime"] = [daytime for daytime in values["daytime"] if daytime in relevant]
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "before")

                case "day":
                #    TODO: Day After
                    daytimes = self.timelines["daytimes"]
                    relevant = [daytime for daytime in daytimes if daytime.day < lookup.value]
                   
                    values["daytime"] = relevant
                    

        
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "before")

                case "room":
                    raise InvalidPreferenceClause("room", "before")
                case "instructor":
                    raise InvalidPreferenceClause("instructoe", "before")

    def except_rule_action(self, rule: Rule, values):
        # For except rule clauses
        lookups = rule.value
        type_ = self.type_
        for lookup in lookups:
            self.on_similar_type(lookup.string_type_, type_)
            match lookup.string_type_:
                case "time":
                    singular_values: list = values['daytime']
                    relevant = [daytime for daytime in singular_values if daytime.time != lookup.value]
                  
                   
                    values['daytime'] = relevant
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "EXCEPT")

                case "day":
                    singular_values: list = values['daytime']
                    relevant = [daytime for daytime in singular_values if daytime.day == lookup.value]
                    [singular_values.remove(r) for r in relevant]
                    values['daytime'] = singular_values
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "EXCEPT")

                case "daytime":
                    values['daytime'].remove(lookup.value)
                    if values['daytime'] == []: raise OverPreferencing(lookup, type_, "EXCEPT")

                case "room":
                    rooms = values["room"]
                    [values["room"].remove(room) for room in rooms if room.identifier == int(lookup.value)]
                    if values['room'] == []: raise OverPreferencing(lookup, type_, "EXCEPT")
                case "instructor":
                    
                   
                    values["instructor"] = [i for i in values["instructor"] if i.identifier != lookup.value]
                    if values['room'] == []: raise OverPreferencing(lookup, type_, "EXCEPT")
                case _:
                    
                    InvalidPreferenceFixing("Unit", "EXCEPT")

 
    def on_similar_type(self, lookup_str, type_):
       
        if lookup_str == type_:
            raise SimilarObjectToPreference(lookup_str, type_)
        return False

    def Output(self):
       
        return self.domain
    