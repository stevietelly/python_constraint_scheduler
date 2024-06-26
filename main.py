from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import PrintTimetable, Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.General.Definition import Definition

Echo.state = True

f = Read("Data/Inputs/mini.json").Extract()
dr = DataReader(f)
dr.Encode()
d= dr.Output()

definition = Definition(d)

statics, dynamics = definition.Output()


c = ConstraintSolver(statics, dynamics, search_rearangement_method = True, search_rearangement_criteria = "least")
c.NodeConsistency()
c.Backtrack()
t = Timetable(c.assignment.Output())
FitnessEvaluation(t, d)



PrintTimetable(t, d).Print()

Write("", "final.json", t.Output()).dump()
