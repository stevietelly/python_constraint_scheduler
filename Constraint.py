"""
Procedure
1. Problem Definition
    a. variables -> static variable
    b. values -> {dynamic variables,... dyanamic variables}
    c. constraints
        i. unary constraints
        ii. binary constraints: Are automatic, they
2. Node consistency: Satisfying Unary Constraints
    a. Eliminate values that do not meet the preferences inside 
"""

from typing import List
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Parser.Reader import DataReader
from Errors.Exception import NoValueFound
from Logic.Structure.Timetable import Timetable
from Logic.Structure.Variables import Static
from Models.ConstraintSatisfaction.Assignment import Assignment
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.ConstraintSatisfaction.Domain import Domain
from Models.General.Definition import Definition
from Models.General.Reductions import PreferencesReduction
from Objects.Academic.Programme import Programme
from Objects.Academic.Units import Unit
from Objects.Persons.Instructor import Instructor


d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()

  


                

                
                

            
            
d = Definition(reader_output)
statics =  d.Output()

cs = ConstraintSolver(statics, reader_output)
cs.NodeConsistency()

cs.Backtrack()
# print(cs.assignment.Output())
Write("", "result.json", Timetable(cs.assignment.Output()).Output()).dump()