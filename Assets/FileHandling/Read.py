import json
import os

from Assets.Functions.Echo import Echo
from Errors.Exception import FileNotFound
echo = Echo()

class Read:
    """
        A class used to read json and text files and returns the contents
        param: filename
        param: filetype
    """
    def __init__(self, filename: str, filetype: str = "json"):
        self.fn = filename
        self.filetype = filetype
        echo.print(f"\nReading File '{filename}'....", color="magenta")
        if not os.path.isfile(filename): raise FileNotFound(filename)


    def _handle_txt(self):
        config = {}
        # open the file in read mode
        with open(self.fn, 'r') as f:
            # read each line in the file
            for line in f:
                # split the line into key-value pairs
                key, value = line.strip().split(': ')
                # convert the value to an integer if it's a number
                if value.isnumeric():
                    value = int(value)
                # add the key-value pair to the dictionary
                config[key] = value

        return config

    def _handle_json(self):
        file = open(self.fn).read()
        content = json.loads(file)
        return content

    def Extract(self)->dict:
        """
        Extract content from files

        return: json
        """
        try:
            return self._handle_json() if self.filetype == "json" else self._handle_txt()
        except BaseException as e:
            print(e)
            exit()
       
