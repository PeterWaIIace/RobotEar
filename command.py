import os
import subprocess
class CommandManager:

    def __init__(self):
        self.config = {
            "get_time"   : "time /T",
            "get_date"   : "date /T"
        }

    def getCommands(self):
        return ','.join(self.config.keys())

    def execute(self, command):
        scriptName = self.config[command]
        output = subprocess.check_output(f"{scriptName}", shell=True)
        return output