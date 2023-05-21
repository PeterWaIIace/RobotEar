import os

class CommandManager:

    def __init__(self):
        self.config = {
            "search" : "search.py",
            "move"   : "move.py",
            "get_time"   : "time /T",
            "get_date"   : "date /T"
        }

    def getCommands(self):
        return ','.join(self.config.keys())

    def execute(self, command):
        scriptName = self.config[command]
        output = os.system(f"{scriptName}")
        return output