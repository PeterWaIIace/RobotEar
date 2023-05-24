
from voiceRecorder import voice2Speech
from command import CommandManager
from brain import ChatBrain
from os.path import exists

import time
import pyttsx3

if __name__ == "__main__":

    print("System is starting.")
    engine = pyttsx3.init()
    cm = CommandManager()

    print("Loading Whisper model.")
    brain = ChatBrain(listOfCommands=cm.getCommands())
    v2s = voice2Speech()
    print("Model loaded.")

    print("Start listening.")
    v2s.listen()

    elapsedTime = 0
    start = time.time()
    text = ""

    while True:
        text = v2s.process()
        print(text)

        if len(text) > 250 or (len(text) and elapsedTime > 5):

            print(f"Processing user input")
            response = brain.process(text)
            print("Response: ", response)
            text = response["response"]
            command = response["command"]

            if command != "None":
                output = cm.execute(command)
                print(f"command output: {output}")
                response = brain.updateCommand(output,command)
                text = response["response"]
                print("Updated response: ", response)
                command = response["command"]

            print("Converting text to speech.")
            v2s.pause()
            engine.say(text)
            engine.runAndWait()
            v2s.start()
            start = time.time()
            v2s.cleanVoiceFile()


        elapsedTime = time.time() - start
        time.sleep(0.01)

    # v2s.close()
