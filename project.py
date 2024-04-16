import os
import sys
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Generator.Generator import DataGenerator
from Data.Parser.Reader import DataReader
from Errors.Exception import InvalidInput
from Logic.Structure.Timetable import PrintTimetable, Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.General.Definition import Definition

echo = Echo()


data_generator  = DataGenerator()

# Generate Data class
def manual_data_generation(input_filename = "data.json"):
    echo.print("\nManually type in data needed....\n", color="green")

    timetable_name = input("Whats the name of the timetable? ")
    instructors = input("How many instructors would you like? ")
    rooms = input("How many rooms would you like? ")
    groups = input("How many groups would you like? ")
    units = input("How many units would you like? ")

    generate_objects(instructors, groups, rooms, units, input_filename, timetable_name)
    return input_filename

def HandlePassedArgs():
    output_file = "final.json"
    input_filename = "data.json"
    srm = False
    srm_type = "least"

    # Search Rearanagement Method
    if "-srm" in sys.argv :
        o_index = sys.argv.index("-srm")
        srm_type = sys.argv[o_index+1]
        srm = True
        if srm_type not in ["most", "least"]: raise InvalidInput("srm", ["least", "most"])

    # for echo
    if "--echo" in sys.argv or "-e" in sys.argv:
        o_index = sys.argv.index("-e") if "-e" in sys.argv else sys.argv.index("--echo")
        state = sys.argv[o_index + 1]
        if state == "off":
            Echo.state = False
        elif not state == "on":
            echo.exit("Invalid Echo status: expected values 'on' or 'off' ")
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)

    # Define output file
    if "-o" in sys.argv or "--output_file" in sys.argv:
        o_index = (
            sys.argv.index("-o")
            if "-o" in sys.argv
            else sys.argv.index("--output_file")
        )
        output_file = sys.argv[o_index + 1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    # Define input file
    if "-i" in sys.argv or "--input_file" in sys.argv:
        i_index = (
            sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--input_file")
        )
        input_filename = sys.argv[i_index + 1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)

    # Manual Data Generation
    if "-mdg" in sys.argv or "--manual-data-generation" in sys.argv:
        manual_data_generation(input_filename)
    
    if "-tdg" in sys.argv or "--text-file-data-generation" in sys.argv:
        if "-tf" in sys.argv or "--text-file" in sys.argv:
            tf_index = (
            sys.argv.index("-tf") if "-tf" in sys.argv else sys.argv.index("--text-file")
            )
            text_input_filename = sys.argv[tf_index + 1]
            sys.argv.pop(tf_index)
            sys.argv.pop(tf_index)
            text_file_data_generation(text_input_filename, output_file)
        else:
            echo.exit("Please insert a text file to read")

    if "run" in sys.argv:
        constraint_solving(input_filename, output_file, srm, srm_type)
    sys.exit()

def text_file_data_generation(text_file:str, filename: str):
    contents = Read(text_file, "txt").Extract()
    generate_objects(contents["instructors"], contents["groups"], contents["rooms"], contents["units"], filename)
    

# convert instructions to Objects
def generate_objects(instructors: int, groups: int, rooms: int, units: int, file_name: str, timetable_name="Testing Timetable"):
    echo.print("Generating Sample input data", color="magenta")
    generate_instructors(instructors)
    generate_rooms(rooms)
    generate_students(groups, int(units))
    generate_units(units, instructors)
    generate_configuration(timetable_name, 5, "Monday", "8am", "4pm", 1)
    write_data_file(file_name)
    return file_name

def generate_configuration(name: str, num_days: int, start_day: str, start_time:str, end_time:str, duration_per_session: int):
    data_generator.GenerateConfiguration(name, num_days, start_day, start_time, end_time, duration_per_session)
    return data_generator.output["configuration"]

def generate_instructors(instructors: int):
    echo.print("Generating Sample input data", color="magenta")
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

def constraint_solving(filename:str, srm, src, output_filename="final.json"):
    data = Read(filename).Extract()
    data_reader = DataReader(data)
    data_reader.Encode()
    data_reader_output = data_reader.Output()
    statics, dynamics = Definition(data_reader_output).Output()
    constraint_solver = ConstraintSolver(statics, dynamics, search_rearangement_method=srm, serach_rearangement_criteria=src)
    constraint_solver.NodeConsistency()
    constraint_solver.Backtrack()

    t = Timetable(constraint_solver.assignment.Output())

    f = FitnessEvaluation(t, data_reader_output)
    Write(os.path.join("Data", "Outputs"), output_filename, f.timetable.Output()).dump()

    PrintTimetable(t, data_reader_output).Print()

def main():
    Echo.state =  True
    input_filename = os.path.join("Data", "Outputs", "data.json")
    if len(sys.argv) > 1: HandlePassedArgs()

    echo.unmute("Automatic Handling\n", color="green")
    f = generate_objects(4, 5, 5, 20, input_filename)
    constraint_solving(f, False, "higher")

if __name__ == "__main__":
    main()