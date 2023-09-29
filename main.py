from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.General.Definition import Definition

Echo.state = True


d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()
definition = Definition(reader_output)
cs = ConstraintSolver(definition.Output(), reader_output, search_rearangement_method=False)
cs.NodeConsistency()
cs.Backtrack()

t = Timetable(cs.assignment.Output())

Write("", "final.json", t.Output()).dump()
print("done.")
