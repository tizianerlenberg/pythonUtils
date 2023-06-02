import os
import json
from pathlib import Path

class Database(dict):
    def __init__(self, filePath, initDict={}):
        self.filePath=Path(filePath).absolute()
        if not os.path.exists(self.filePath):
            with open(self.filePath, 'w') as file:
                file.write(json.dumps(initDict))
        super(Database,self).__init__({})
        self.loadFromBase()
                
    def loadFromBase(self):
        with open(self.filePath, 'r') as file:
            content = file.read()
            if content != "":
                self.replaceDict(json.loads(content))
            else:
                self.replaceDict({})
                
    def saveToBase(self):
        with open(self.filePath, 'w') as file:
            file.write(json.dumps(self, indent=4))
            
    def replaceDict(self, setDict):
        super(Database,self).clear()
        super(Database,self).update(setDict)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.saveToBase()
