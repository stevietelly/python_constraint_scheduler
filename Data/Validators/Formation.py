"""
Data validator
"""

import sys


class DataValidator:
    def __init__(self, data_structure: list | dict, data_entry: list | dict):
        self.data_structure = data_structure
        self.data_entry = data_entry
    
    def ValidateList(self)->bool:
        for datum in self.data_entry:
            if not datum in self.data_structure:
                return False
        return True

    def ValidateDictionary(self)->bool:
        # Check that all required keys are present and have the correct types
        for key, value_type in self.data_structure.items():
            if key not in self.data_entry:
                return False
                # raise ValueError(f"Missing required key: {key}")
            if not isinstance(self.data_entry[key], value_type):
                return False
                # raise TypeError(f"Invalid type for key '{key}', expected {value_type.__name__}")
        
        # Check that all values are valid, but ignore any additional keys
        for key in self.data_entry:
            if key not in self.data_structure:
                continue
            value_type = self.data_structure[key]
            if not isinstance(self.data_entry[key], value_type):
                return False
                # raise TypeError(f"Invalid type for key '{key}', expected {value_type.__name__}")
        
        # If all checks pass, return True to indicate success
        return True

    def Validate(self)->bool:
        if type(self.data_entry) == list and type(self.data_structure) == list:
            return self.ValidateList()
        elif type(self.data_entry) == dict and type(self.data_structure)== dict:
            return self.ValidateDictionary()
        else:
            print("Invalid Input Types ", f"{type(self.data_entry)} against {type(self.data_structure)}")
            sys.exit(1)