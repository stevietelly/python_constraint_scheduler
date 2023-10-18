from copy import deepcopy
from typing import List
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Parser.Reader import DataReader
from Logic.Compliance.Negative import Clash, GroupClash, RoomClash, InstructorClash
from Logic.Compliance.Positive import FreeInstructorPeriod, FreePeriod, FreeGroupPeriod, FreeRoomPeriod
from Logic.DateTime.DayTime import DayTime
from Logic.Statistics.Calculators import GroupCalculator, InstructorCalculator, RoomCalculator
from Logic.Statistics.Costs.Cost import ClashCost, PreferenceSatisfacionCost
from Logic.Structure.Session import Session
from Logic.Structure.Timetable import Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.Evaluation.Checks import RuleCheck
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.General.Definition import Definition
from Objects.Internal.Preference.Preference import All, And
from Objects.Persons.Instructor import Instructor
from Objects.Persons.Students import Group
from Objects.Physical.Rooms import Room
from prettytable import PrettyTable

Echo.state = False


d = DataReader(Read("Data/Inputs/minified.json").Extract())
d.Encode()
reader_output = d.Output()

d = Definition(reader_output, True)

cs = ConstraintSolver(d.Output(), reader_output,search_rearangement_method=True, choose_instructors=d.choose_instructors, search_rearangement_criteria="least")

cs.NodeConsistency()
cs.Backtrack()

t = Timetable(cs.assignment.Output())




