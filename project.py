from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Data.Generator.Generator import DataGenerator
from Data.Parser.Reader import DataReader
from Logic.Structure.Timetable import PrintTimetable, Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.General.Definition import Definition


data_generator  = DataGenerator()


# convert instructions to Objects
def generate_objects(instructors: int, groups: int, rooms: int, units: int, file_name: str):
    generate_instructors(instructors)
    generate_rooms(rooms)
    generate_students(groups, units)
    generate_units(units, instructors)
    generate_configuration("Testing Timetable", 5, "Monday", "8am", "4pm", 1)
    write_data_file(file_name)
    return data_generator.output

def generate_configuration(name: str, num_days: int, start_day: str, start_time:str, end_time:str, duration_per_session: int):
    data_generator.GenerateConfiguration(name, num_days, start_day, start_time, end_time, duration_per_session)
    return data_generator.output["configuration"]

def generate_instructors(instructors: int):
    data_generator.GenerateInstructors(instructors)
    return data_generator.output["instructors"]

def generate_rooms(no_of_rooms: int):
    data_generator.GenerateRooms(no_of_rooms)
    return data_generator.output["rooms"]

def generate_units(no_of_units: int, no_of_instructors: int):
    data_generator.GenerateUnits(no_of_units, no_of_instructors)
    return data_generator.output["units"]

def generate_students(no_of_groups: int, no_of_units: int):
    data_generator.GenerateGroups(no_of_groups, no_of_units)
    return data_generator.output["groups"]

def write_data_file(filename: str):
    data_generator.output_file = filename
    data_generator.write()

def constraint_solving(filename:str):
    data = Read(filename).Extract()
    data_reader = DataReader(data)
    data_reader.Encode()
    data_reader_output = data_reader.Output()
    define = Definition(data_reader_output)
    
    constraint_solver = ConstraintSolver(define.Output(), data_reader_output, search_rearangement_method=True)
    constraint_solver.NodeConsistency()
    constraint_solver.Backtrack()

    t = Timetable(constraint_solver.assignment.Output())

    f = FitnessEvaluation(t, data_reader_output)
    Write("./", "final.json", f.timetable.Output()).dump()
    PrintTimetable(t, data_reader_output).Print()

def main():
    generate_objects(4, 5, 5, 20, "data.json")
    constraint_solving("data.json")

if __name__ == "__main__":
    main()
