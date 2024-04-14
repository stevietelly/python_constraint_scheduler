# Constraint Solver

## Introduction

A constraint Solver is the basic solution to a Constraint Programming whereby the solver searches a solution problem in an attempt to find an optimal solution while maitining `constraints`

The solution offered in this project tries to tackle **timetables** or **scheduling** (as a general concept)

I tackled this with  `node consistency` and `recursive backtracking` in that order

## Node Consistency

Node Consistency aims to satisfy unary constraints for variables in a search space *domain.* In this case taking whatever preference each session is affected by from the individual "`Objects`" (`Unit`, `Instructor`, `Group` and `room`) and eliminates them in the domain space.

This does not necessarily create a complete an assignment but is the only process where the preferences can be maintained.

## Recursive Backtracking

Recursive Backtracking loops through al static variables and tries to find an acceptable value for each by looping through its domain.
![Constraint Solver Diagram](CosntraintSolver.png "Constraint Solver Diagram")
