import time
import random
import sys
import os
import glob
import json
import calendar
from datetime import datetime
sys.path.append(os.path.abspath('..'))

from brain import ChatBrain

def test_commands():
    cb = ChatBrain()
    response = cb.completion2Dict("RESPONSE: I'm sorry, I don't understand what you mean. Could you please rephrase your command? \nCOMMAND: None")

    print(response)
    assert(response["response"] == " I'm sorry, I don't understand what you mean. Could you please rephrase your command? \n")
    assert(response["command"] == "None")