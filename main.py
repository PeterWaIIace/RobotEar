
from voiceRecorder import voice2Speech
from brain import ChatBrain
from os.path import exists

import time
import pyttsx3

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

        if len(text) > 250 or (len(text) and elapsedTime > 5):
            response = brain.process(text)
            text = response["response"]
            command = response["command"]

            engine.say(text)
            engine.runAndWait()
            start = time.time()
            v2s.cleanVoiceFile()

        elapsedTime = time.time() - start
        time.sleep(0.01)

    v2s.close()
