
from voiceRecorder import voice2Speech
import time
import json
import openai
import pyttsx3

from os.path import exists
class ChatBrain():

    def __init__(self,listOfCommands="search,look,sleep",configFile="config.json"):

        self.listOfCommands = listOfCommands
        config = {"organization":"","apiKey":""}
        with open(configFile, "r") as f:
            config = json.load(f)

        openai.organization = config["organization"]
        openai.api_key = config["apiKey"]


    def process(self, prompt):
        messages = [
            {"role" : "system", "content" :
             f"You are robot processing speech commands. User will communicate with text transcribed from speech."\
             f"If you will detect that user want any of following actions `{self.listOfCommands}`, then you need to fill COMMAND field with it." \
             f"If none of commands is detected, then respond to user and fill COMMAND field with None." \
             f"Follow that response pattern: RESPONSE: <Robot Response> COMMAND: <Robot command>"
            },
            {
              "role" : "user",
              "content" : f"User transcribed speech: `{prompt}` "
            }
            ]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.75,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return completion["choices"][0].message


if __name__ == "__main__":

    engine = pyttsx3.init()
    brain = ChatBrain()
    v2s = voice2Speech()
    v2s.listen()


    elapsedTime = 0
    start = time.time()
    text = ""
    for n in range(100000):
        text = v2s.process()
        print(text)

        if len(text) > 250 or (len(text) and elapsedTime > 10):
            print(f"text: {text}")
            response = brain.process(text)["content"]

            print(response)
            engine.say(response)
            engine.runAndWait()
            start = time.time()
            v2s.cleanVoiceFile()

        elapsedTime = time.time() - start
        time.sleep(0.01)

    v2s.close()
