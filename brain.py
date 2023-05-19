
import re
import json
import openai

from os.path import exists
class ChatBrain():

    def __init__(self,listOfCommands="search,look,sleep",configFile="config.json"):

        self.listOfCommands = listOfCommands
        config = {"organization":"","apiKey":""}
        with open(configFile, "r") as f:
            config = json.load(f)

        openai.organization = config["organization"]
        openai.api_key = config["apiKey"]

        self.messages = [
            {
             "role" : "system",
             "content" :
             f"You are robot processing speech commands. User will communicate with text transcribed from speech."\
             f"If you will detect that user want any of following actions `{self.listOfCommands}`, then you need to fill COMMAND field with it." \
             f"If none of commands is detected, then respond to user and fill COMMAND field with None." \
             f"Follow that response pattern: RESPONSE: <Robot Response> COMMAND: <Robot command>"
            }
        ]

    def __extractResponse(self,text):
        print(f"{type(text)}, {text}")
        pattern = r'(?<=RESPONSE:).*(?=COMMAND)'
        match = re.search(pattern, text, re.DOTALL)
        print(match)
        if match:
            return match.group(0)
        else:
            return None

    def __extractCommand(self,text):
        print(f"{type(text)}, {text}")
        pattern = r'(?<=COMMAND: ).*'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(0)
        else:
            return None

#   RESPONSE: The current time is <current time>. 
#   COMMAND: None
    def completion2Dict(self,message):
        response = self.__extractResponse(message)
        command = self.__extractCommand(message)

        return {"response":response,"command":command}

    def process(self, prompt):
        self.messages.append(
            {
              "role" : "user",
              "content" : f"User transcribed speech: `{prompt}` "
            }
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.75,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        self.messages.append({
            "role":"assistant",
            "content": completion["choices"][0].message['content']
        })

        return self.completion2Dict(completion["choices"][0].message['content'])