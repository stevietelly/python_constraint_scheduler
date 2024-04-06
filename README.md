# Python Constraint Scheduler
___

A Constraint scheduler Implementation in Python that leverages optimization to form solutions that are better.


## Introduction
A simple Timetable generator software based on an ongoing personal project. 

The project is geared at developing an application that deveolops timetables based on input data and recommendations given,
finding the most optimum solution to a timetable that has the most minimum number of clashes and meets user demands to the
most physically possible.

It takes use of costs and evaluation function to find the optimum solution by satisfying constratints(prferences and priorities)


## Definition of Terms
Ther are specific terms used in the entire project that may cause some confusion, the following are ther definitions

**Instructors**     This term is used to encompass any individual that teaches i.e lecturers, professors

**Students**        This term is used to refer to learner who will be involved in beong taught by the instructors

**Group**           This term reffers to a collection of students with the same course and year

**Unit/Module**     This term is used to refer to the 'subject' being taught

**Programmes**      Reffers to a title that encompasses a group of students segragated in the years they were enrolled

**Rooms**           Reffers to a physical enclosure or place where learning activities take place

**optimization**    Reffers to reducuing clashes of all kind

**saturation**      This term reffers when the program has eradicated all possible clashes possible to the point of no more optimizations to be made

**maximum Limit**   The upper limit in number of loops that can be made

**schedule**        this is a capsule(python class) holding the unit, a group of students and a single instructor

**session**         This is a capsule(python calss) holding a schedule, a time and a day

**constraints**     These are rules that a timetable is required to fullfill, categorised into soft constraints and hard constraints

**preference**      This is a user recommnded constraint that define what they would want

**priorities**      This refers to the preferences levels and which will be considered first to last

## Development Methodology
There are different mehods for handling timetable generation and each comes with its strengths and weaknesses but i preferred 
to develop a hybrid algorithim that takes concepts from three other algorithims

- **Genetic Algorithims**                   -is a search heuristic that is inspired by the process of natural selection, involving creating a population of candidate solutions and using evelutionary operaters such as selection, crossover and mutation to eveolve towards an optimal solution

- **Tabu Search Algorithim**                -Is a metaheuristic algorithim that uses local search to iteratively explore the neighbourhood for a better solution. a tabu list is kept for the moves that have been tried before and deemed unproductive.

- **Constraint Satisfaction Algorithim**    -Is is an algorithim that is used to optimize problem subject to a set of constraints while minimizing and maximizing the ibjective function

The algorithim is to use the following techniques
- **Encoding**                -Representing concepts as a data structure that can be manipuated algorithimically

- **Fitness Evaluation**      -It is a function that evaluates how well a acandidate solution satisfies the requirements
- **Constraint Satisfaction** -Finding a solution that meets a specific set of constraints
- **selection**               -It is the process of selecting candidate solutions from the population for further evolution
- **crossover**               -It is a geneetic operator that comines two parent solutions to comeup with a new child solution
- **mutation**                -It is a genetic opeartor that 

### Constraints
Constraints will be a list of rules that define the generation of the final timetable
they will be divided into two type of constraints
1. *soft*
2. *hard*

The constraints will be hard encoded to the algorithim or some will be expexted to be filled in by the user
in form of preferences

#### Hard Constraints
These are constraints thar must be strictly satisfied for the timetable to be satisfied, they are non-neogotiable
1. Minimise Conflicts(clashes)
    > - *Each Teacher can only teach one class at a time*
    > - *Each Room can only be used one session at a time*
    > - *Each Group of students can only attend one session at a time*
2. Class Capacity - All sessions must happen in a room that can fit the number of students available in a group
3. Class one priorities - the preferences set as level one priorit and level two priority must be met

#### Soft Constraints
1. Level Three and Level Four Priorities - the preferrnces set as level three and four priority
2. Consecetive classes 
    > - *Minimize student consecutive classes*
    > - *Minimize teacher consecutive classes*
    > - *Minimize room consecutive classes*

### Priorities and Preferences
Both are crucial in timetable generation and play an important role in constraint satisffaction to objective evaluation

priorities define order of preferences, that is whose preferences come firts while preferences are a list of rules that are encoded to
define what the user wants.

### Preference Handling
for the sake of representing preferences, classes have been made to hard encode them into the program.

But issue come when we have to represent them in the json files, so i have to find a way to standardise the rules for 
compatibility with a parser that will convert them to python objects.

The following rules are present in the current system
> - **Before** - this was made to represent periods before a specific period
> - **After** -     This was made to represent periods after a spacific period
> - **Except** -    All Except the list passed in the argument
> - **All** - All values present can be used
> - **Only** - Only use the values passed

The below are conjuctions that supplement the above rules
> - **And** - used to join two rules that are to be satisfied together
> - **Or** - used to join two rules that one can be satisfied instead of the other

### Preference Syntaxing
The following is the syntax for encoding prefernce on json files

```
{} - preferences are defined inside these
[] - any other objects are defined inside these 
BEFORE
AFTER
ALL
ONLY
EXCEPT

AND
NOT

Example:

Before 4:00pm
{BEFORE [TIME:->'4:00PM']}


Before monday and after WEDNESDAY
{BEFORE [DAY:->'Monday'] AND AFTER [DAY:->'WEDNESAY']}

All rooms
{ALL [ROOM]}

All rooms except room A15
{EXCEPT [ROOM:->'A15']}

Only rooms A15 and A20
{ONLY [ROOM:->'A15'], [ROOM:'A20']}
```





