# Preference Handling

## Introduction

for the sake of representing preferences, classes have been made to hard encode them into the program.

But issue come when we have to represent them in the json files, so i have to find a way to standardise the rules for

compatibility with a parser that will convert them to python objects.

## Preference Rules

The following rules are present in the current system

> - **Before** - this was made to represent periods before a specific period

> - **After** -     This was made to represent periods after a spacific period

> - **Except** -    All Except the list passed in the argument

> - **All** - All values present can be used

> - **Only** - Only use the values passed

The below are conjuctions that supplement the above rules

> - **And** - used to join two rules that are to be satisfied together

> - **Or** - used to join two rules that one can be satisfied instead of the other (depreceated)

## Preference Syntaxing

The following is the syntax for encoding prefernce on json files
 > - `{}` - preferences are defined inside these

 > - `[]` - individual object constrainsts are defined inside these

currently supported objects:`UNIT`, `TIME`, `DAYTIME`, `DAY`, `ROOM`, `GROUP`

Example:
|Explanation|Prefrence String|
| ---- | ---- |
|Before 4:00pm| `{BEFORE [TIME:->'4:00PM']}`|
|Before monday and after WEDNESDAY| `AND {BEFORE [DAY:->'Monday']}, {AFTER [DAY:->'Wednesday']}`|
|Only at 2:00pm, 3:00pm and 8:00am and only unit 1|`AND {ONLY [TIME:->'2:00pm'], [TIME:->'3:00PM']}, {ONLY [TIME:->'8:00am']}, {EXCEPT [UNIT:->'1']}`|
|All rooms except room A15|`{EXCEPT [ROOM:->'A15']}`|
|Only rooms A15 and A20|`{ONLY [ROOM:->'A15'], [ROOM:'A20']}`|



