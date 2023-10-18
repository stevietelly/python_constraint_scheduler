import sys
from typing import List, Dict, Any
from Assets.FileHandling.Read import Read
from Assets.FileHandling.Write import Write
from Assets.Functions.Echo import Echo
from Data.Parser.Reader import DataReader
from Data.Validators.Structure import INPUT_FILE_UNITS
from Data.Validators.Type import FileTypeValidator
from Data.Validators.Utilities import algorithm_type_validator, confirm_file_path, is_valid_day, is_valid_formart, is_valid_time, return_list_of_days
from Data.Generator.Generator import DataGenerator
from Errors.Exception import InvalidInput
from Logic.Structure.Timetable import PrintTimetable, Timetable
from Models.ConstraintSatisfaction.ConstraintSolver import ConstraintSolver
from Models.Evaluation.Fitness import FitnessEvaluation
from Models.General.Definition import Definition



#  Input Files holder
input_files: Dict[str, str]= {"configurations": "Data/Defaults/configuration.json", "students": "Data/Defaults/students.json", "instructors": "Data/Defaults/instructors.json", "rooms": "Data/Defaults/rooms.json", "units": "Data/Defaults/units.json", "courses": "Data/Defaults/courses.json"}

custom_config: Dict[str, Any] = {
  "name": str,
  "days":  list,
  "start-time": str,
  "end-time": str,
  "duration-per-session": int,
  "system": {
    "limit": int,
    "saturation": bool,
    "tries": int,
    "output": str,
    "output_folder": str
  }
}

echo = Echo()
def main():

    # for echo
    if "--echo" in sys.argv or "-e" in sys.argv:
        o_index = sys.argv.index("-e") if "-e" in sys.argv else sys.argv.index("--echo")
        state = sys.argv[o_index+1]
        if state == "on":
            Echo.state = True
        elif not state == "off":
            echo.exit("Invalid Echo status: expected values 'on' or 'off' ")
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)

    # For generating mock data for testing
    if "-dg" in sys.argv or "--data_generator" in sys.argv:
        generateData()
    
    if "run" in sys.argv:
        Run()
  
    echo.exit("Invalid inputs: Read README file for input paramaters")
          
def write_configuration_manually():
    """
    Manually write the configuration
    """
    echo.unmute("Timetable Inputs", color="yellow")
    config_list = {"name": str, "days": int, "start-day": str, "start-time": str, "end-time": str,"duration-per-session": int}
    for config in config_list.keys():
        while True:
            input_str = input(config+": ")
            try:
                
                config_list[config] = input_str
                if type(config_list[config]) == type(input_str):
                    break
                
            except:
                echo.exit("Invalid input type", 2)   
             

    echo.unmute("Sytem Inputs Inputs", color="yellow")
    system_inputs = {
    "limit": int,
    "saturation": bool,
    "tries": int,
    "output": str,
    "output_folder": str
    }

    for system_input in system_inputs:
        while True:
            input_str_sys = input(system_input+": ")
            try:
                system_inputs[system_input] = input_str_sys
                break
            except:
                echo.exit("Invalid input type")   
               
    
    print("\nValidating input...........\n")
    
    if not is_valid_day(config_list["start-day"]):
        echo.exit("\nInvalid day -> ", config_list["start-day"])
       

    custom_config["days"] = return_list_of_days(config_list["start-day"], config_list["days"])

    if not is_valid_time(config_list["start-time"]):
        echo.exit("\nInvalid Time -> ", config_list["start-time"])
 

    if not is_valid_time(config_list["end-time"]):
        echo.exit("\nInvalid Time -> ", config_list["end-time"])
     
def Run():
    input_file: str
    output_file: str
    output_type: str
    srm: bool = False
    srm_type: str 
    ci: bool

    # Define input file
    if "-i" in sys.argv or "--input_file" in sys.argv:
        o_index = sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--input_file")
        input_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    elif "defaults" in sys.argv:
        input_file = "Data/Inputs/mini.json"
    else:
        echo.exit("please Link in an input file, or run defaults")

    # Define output file
    if "-o" in sys.argv or "--output_file" in sys.argv:
        o_index = sys.argv.index("-o") if "-o" in sys.argv else sys.argv.index("--output_file")
        output_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    else:
        echo.exit("Please Define an Output file")
    
     # Output Type for the final output
    if "-tp" in sys.argv or "--output_type" in sys.argv:
        o_index = sys.argv.index("-tp") if "-tp" in sys.argv else sys.argv.index("--output_type")
        output_type = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    else:
        output_type = "json"

    Echo().print("Validating Input File.........")

    if not is_valid_formart(output_type):
        echo.exit("invalid output formart: Please Read Info for specified output formarts")
    
    data = Read(input_file).Extract()
    if not FileTypeValidator(data):
        echo.exit("Invalid Input File")
    

    if "-srm" in sys.argv :
        o_index = sys.argv.index("-srm")
        srm_type = sys.argv[o_index+1]
        srm = True
        if srm_type not in ["highest", "least"]: raise InvalidInput("srm", ["least", "highest"])
    else:
      
        srm = False
        srm_type = None

    if "-ci" in sys.argv :
        o_index = sys.argv.index("-ci")
        ci = True
    else:
        ci = False

    reader = DataReader(data)
    reader.Encode()
    reader_output = reader.Output()
    
    d = Definition(reader_output, ci)
  
    cs = ConstraintSolver(d.Output(), reader_output, search_rearangement_method=srm, choose_instructors=ci, search_rearangement_criteria=srm_type)

    cs.NodeConsistency()
    cs.Backtrack()

    t = Timetable(cs.assignment.Output())

    f = FitnessEvaluation(t, reader_output)
    Write("./", "final.json", f.timetable.Output()).dump()
    PrintTimetable(t, reader_output).Print()
    exit()

    
def generateData():
    echo.unmute("Genarate mock data", color="light_magenta")
    input_file:str|None = None
    output_file:str|None = None

    # Define output file
    if "-o" in sys.argv or "--output_file" in sys.argv:
        o_index = sys.argv.index("-o") if "-o" in sys.argv else sys.argv.index("--output_file")
        output_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
        
    # Define input file
    if "-i" in sys.argv or "--input_file" in sys.argv:
        o_index = sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--input_file")
        input_file = sys.argv[o_index+1]
        sys.argv.pop(o_index)
        sys.argv.pop(o_index)
    while True:
        if not output_file:
            output_file = input("Enter name of output file: ")
        echo.unmute("1. Use a text File\n2. Input Manually")
        choice = input("Pick one of the above: ")

        generator = DataGenerator(output_file)
        
        inputs = None if input_file is None else Read(input_file).Extract()
        match choice:
            case '1':
                echo.print("\nGenerating Data from a text file....\n", color="green")
                file_ = input("Input Text File path: ")
                inputs = Read(file_, "txt").Extract()
                generator.GenerateAllInputData(inputs["instructors"], inputs["groups"], inputs["units"], inputs["rooms"], custom_config)
                generator.write()
                
            case '2':
                echo.print("\nManually type in data needed....\n", color="green")

                instructors = input("How many instructors would you like? ") if not input_file else int(inputs["instructors"])
                rooms = input("How many rooms would you like? ") if not input_file else int(inputs["rooms"])
                groups = input("How many groups would you like? ") if not input_file else int(inputs["groups"])
                units = input("How many units would you like? ") if not input_file else int(inputs["units"])

        if "-c" in sys.argv or "--configuration" in sys.argv:
            o_index = sys.argv.index("-c") if "-c" in sys.argv else sys.argv.index("--configuration")
            config = Read(sys.argv[o_index+1]).Extract()
            sys.argv.pop(o_index)
            sys.argv.pop(o_index)
            generator.GenerateAllInputData(instructors, groups, units, rooms, config)
            generator.write()
        else:
            write_configuration_manually()        
            generator.GenerateAllInputData(instructors, groups, units, rooms, custom_config)
            generator.write()
            
        sys.exit()
            

if __name__ == "__main__":
    main()