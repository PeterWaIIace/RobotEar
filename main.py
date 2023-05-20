
from voiceRecorder import voice2Speech
from command import CommandManager
from brain import ChatBrain
from os.path import exists

import time
import pyttsx3

if __name__ == "__main__":

    engine = pyttsx3.init()
    cm = CommandManager()
    brain = ChatBrain(listOfCommands=cm.getCommands())
    v2s = voice2Speech()
    v2s.listen()

    elapsedTime = 0
    start = time.time()
    text = ""
    for n in range(100000):
        text = v2s.process()
        print(text)

        if len(text) > 250 or (len(text) and elapsedTime > 5):
            response = brain.process(text)
            print(response)
            text = response["response"]
            command = response["command"]

            if command != "None":
                output = cm.execute(command)
                print(f"command output: {output}")
                response = brain.updateCommand(output,command)
                text = response["response"]
                command = response["command"]

            v2s.pause()
            engine.say(text)
            engine.runAndWait()
            v2s.start()
            start = time.time()
            v2s.cleanVoiceFile()


        elapsedTime = time.time() - start
        time.sleep(0.01)

    v2s.close()
