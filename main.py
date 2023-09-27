from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.General.Definition import Definition







d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()

definition = Definition(reader_output)
cs = ConstraintSolver(definition.Output(), reader_output)
cs.NodeConsistency()
cs.Backtrack()

Timetable(cs.assignment.Output())

