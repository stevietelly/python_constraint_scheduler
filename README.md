# Python Constraint Scheduler

## Introduction

A Timetable generator using `Constraint Programming` to develop optimum solutions while still
taking into account user preferences.The project is built with expansion in mind, to be able to
incoparate more algorithms in thefuture.

This is done by first represnting the initial values in a json file, after which an encoder
converts it into Objects that the algorithim can understand and use to find a solution.
The Objects include:

    1.`Room`
    2. `Instructor`
    3. `Group`
    4. `Unit`

## Definition of terms

- **Room** - An Object that represents the physical space where an action takes place
- **Instructor** - An Object that represents a person in charge
- **Group** - An Object that represents an audience
- **Unit** - An Object that represents a module to be taught
- **Session** - A fully filled Object containing a `Unit`, `Group`, `Time`, `Day`, `instructor` and `room`
- **Timetable** - A collection of completed `sessions`
- **Constraint Solver** - A `Constraint Programming` algorithm
- **Encoding** - Converting into an organised formart
- **Fitness Evaluation** - Checking how good a timetable is
- **Preference** - A user defined constraint, read `Preferences.md` for more
- **Variable** - A structure that defines an object that requires to be given
- **value** - An Object containing a single `Room` and  `DayTime`
- **assignment** A structure containg all the variables and their acompapaning values
- **Domain** - A structure that contains the `values` a `variable` can take

## Process

1. **Reader**
   - Convert Json File into python dictionaries, lists etc
2. **DataReader**
   - Encoding to the different Objects and reading configuration
3. **Definition**
   - Divide the differrent Objects into
4. **Constraint Solver**
   - A constraint Programming implementation to solve the problem, read  *`ConstraintProgramming.md`* for more
5. **Fitness Evaluation**
   - An implementation to test how goos the solution is
6. **Timetable Printer (terminal)**
   - Printing to the screen(Command Line)

> *Works optimally for days not exceeding three*

7. **Writer**
   - writes the timetable to a `json` file

![1713015015863](image/README/1713015015863.png "Complete Process Diagram")
