
from voiceRecorder import voice2Speech
import time
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


    def process(self, prompt):
        messages = [
            {"role" : "assistant", "content" : f"robot brain processing speech commands, if found any of the following {self.listOfCommands} commands, inform user of its execution. Commands can come chaotic, so robot need to try guess closest one."},
            {"role" : "user", "content" : f"{prompt}"}
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

    brain = ChatBrain()
    v2s = voice2Speech()
    v2s.listen()

    elapsedTime = 0
    start = time.time()
    text = ""
    for n in range(100000):
        text += v2s.process()
        print(text)

        if len(text) > 30 or (len(text) and elapsedTime > 10):
            print(f"text: {text}")
            print(brain.process(text))
            text = ""
            start = time.time()

        elapsedTime = time.time() - start
        time.sleep(0.01)

    v2s.close()
