from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.ConstraintSatisfaction.NodeConsistency import NodeConsistency
# from Models.Generator.Generator import Generator






d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()
# cs = ConstraintSolver(reader_output)
# cs.node_consistency()
# cs.StaticSetting()
# cs.AC_3()
# cs.Assesion()
# sessions = cs.Output()
# timetable = Timetable(sessions).Output()

# Write("Output/", "timetable.json", timetable).dump()


NodeConsistency()

# NodeConsistency(reader_output).Consistency()
# g = Generator(output)
# g.Initialise()
# g.Schedule()

# schedules, sessions, timelines = g.Output()

# ConstraintSolver(schedules, sessions, timelines, output).enforce_node_consistency()

