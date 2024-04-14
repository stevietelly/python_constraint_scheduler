from Data.Parser.Preferences import PreferenceParser
from Errors.Error import InvalidPreferenceFixing, MissingValueInPreference
from Logic.DateTime.Day import Day
from Logic.DateTime.DayTime import DayTime
from Logic.DateTime.Time import Time
from Objects.Persons.Instructor import Instructor
from Objects.Physical.Rooms import Room
from Objects.User.Preference.Preference import Except, Rule


# preferences = ["{BEFORE [TIME:->'4:00PM']}", "​AND {BEFORE [DAY:->'Monday']},  {AFTER [DAY:->'WEDNESAY']}", "AND {ONLY [TIME:->'2:00pm'], [TIME:->'3:00PM']}, {ONLY [TIME:->'8:00am']}, {EXCEPT [UNIT:->'1']}"]

# result = []
# for preference in preferences:
#     result.append(PreferenceParser(preference).Parse())


t = Time("0:00am")
days = [Day("Monday", t, t), Day("Tuesday", t, t), Day("Wednesday", t, t)]
times = [Time("8:00am"), Time("9:00am"), Time("10:00am"), Time("11:00am"), Time("12:00pm")]
values = {
    'daytime': [DayTime(day, time) for day in days for time in times],
    'room': [Room(1, "A1", 40, None), Room(2, "A2", 40, None), Room(3, "A3", 40, None)],
    'instructor': [
        Instructor("Stephen Telian", "Mr.", 1, None),
        Instructor("Stanton Collins", "Mr.", 1, None), 
        Instructor("Elizabeth Banks", "Mr.", 1, None), 
        Instructor("Elizabeth Banks", "Mr.", 1, None), 
        Instructor("Elizabeth Banks", "Mr.", 1, None), 
        Instructor("Elizabeth Banks", "Mr.", 1, None)]
    }

rule = PreferenceParser("{ONLY [DAYTIME:->'Monday at 8:00am'], [DAYTIME:->'Tuesday at 8:00am'], [ROOM:->'1'], [UNIT:->'1']}").Parse()



def only_rule_action(rule, value):
    print(rule)
    # For except rule clauses
    lookups = rule.value
    values['daytime'] = [lk for lk in lookups if lk.string_type_ == "daytime"]

    for lookup in lookups:
        match lookup.string_type_:
            case "time":
                singular_values: list = values['daytime']
                
                if all([lookup.value == v.time for v in singular_values ]): MissingValueInPreference("Unit", "Only", lookup.value)
                relevant = [daytime for daytime in singular_values if daytime.time != lookup.value]
                [singular_values.remove(r) for r in relevant]
                values['daytime'] = singular_values
            case "day":
                singular_values: list = values['daytime']
                # If the value is missing
                if all([lookup.value == v.day for v in singular_values ]): MissingValueInPreference("Unit", "Only", lookup.value)
                relevant = [daytime for daytime in singular_values if daytime.day != lookup.value]
                [singular_values.remove(r) for r in relevant]
                values['daytime'] = singular_values
            case "daytime":
                continue
            
            case "room":
                rooms = values["room"]
                [values["room"].remove(room) for room in rooms if room.identifier == int(lookup.value)]
            # case _:
            #     InvalidPreferenceFixing("Unit", "EXCEPT")
    return values


print(only_rule_action(rule, values))

