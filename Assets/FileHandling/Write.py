import json
from typing import Union


class Write:
    def __init__(self, filepath: str, filename:str, content: Union[dict, list], type_="json"):
        """
        A class to save content to file
        :param filepath: the location of the file
        :str filepath: 
        """
        self.fn = filename
        self.cont = content
        self.type_ = type_
        self.fp = filepath

    def dump(self):
        if self.type_ == "json":
            self.dumpJSON()
        elif self.type_ == "html":
            self.dumpHTML()

    def dumpJSON(self):
        
        d = json.dumps(self.cont, indent=1)
        with open(self.fp + self.fn, 'w') as f:
            f.write(d)

    def dumpHTML(self):
        # create stylesheet
        open(f'{self.fp}/css/style.css', 'w')
        f = open(self.fp + self.fn, 'w')
        f.write(self.cont)
