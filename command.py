import os

class CommandManager:

    def __init__(self):
        self.config = {
            "search" : "search.py",
            "move"   : "move.py",
            "find"   : "search.py"
        }

    def getCommands(self):
        return ','.join(self.config.keys())

    def execute(self, command):
        scriptName = self.config[command]
        os.system(f"./{scriptName}")