"""
Type Validator
"""

import sys

from Data.Validators.Formation import DataValidator
from Data.Validators.Structure import INPUT_FILE_STRUCTURE, INPUT_FILE_UNITS




class FileTypeValidator:
    def __init__(self, data: dict, filetype:str="input") -> None:
        self.data = data
        self.filetype = filetype
       
        if not filetype in ["input", "output"]:
            sys.exit(f'Uknown File Type({filetype})')

       
       
    def ValidateInput(self)->bool:
        keys = list(self.data.keys())
        if not DataValidator(INPUT_FILE_UNITS, keys).Validate():
            return False
        for struct in INPUT_FILE_UNITS:
            data_structure = INPUT_FILE_STRUCTURE[struct]
            for datum in self.data[struct]:
                if not DataValidator(data_structure, datum):
                    return False
        
        return True

    def ValidateOutput(self)->bool:
        pass

    def ValidateFile(self)->bool:
        if self.filetype == "input":
            return self.ValidateInput()
        elif self.filetype == "output":
            return self.ValidateOutput()
