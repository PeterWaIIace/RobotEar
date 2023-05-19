from queue import Queue
import numpy as np
import whisper
import wave
import time
import sys

import soundfile as sf
import pyaudio
import os

from sys import platform

class voice2Speech:

    def __init__(self):
        # chunk = 1024  # Record in chunks of 1024 samples
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        # fs = 16000  # Record at 44100 samples per second
        # seconds = 3
        self.tmp_path = "tmp_audio"
        self.filename = "output.wav"
        self.fileIterator = 0
        self.maxFiles = 10
        self.stop = False
        self.max_buff_size = self.fs*10
        self.frames = np.array([[],[]])
        self.model_whisper = whisper.load_model("base.en")
        self.accepted_prob = 0.5
        self.audio_path = "tmp_stream.wav"


    def __callback(self,in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        audio_data = np.array([audio_data[1::2],audio_data[::2]])
        self.frames = np.append(self.frames,audio_data,axis=1)
        return (in_data, pyaudio.paContinue)

    def listen(self):
        # Instantiate PyAudio and initialize PortAudio system resources (2)
        self.p = pyaudio.PyAudio()

        # Open stream using callback (3)
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=self.channels,
                        rate=self.fs,
                        input=True,
                        stream_callback=self.__callback)

    def process(self):
        predicted_texts = ""
        tmp_frames = self.frames.copy()

        # Write wav data to the temporary file as bytes.
        sf.write(f"{self.audio_path}",tmp_frames.T,self.fs)

        if os.path.exists(self.audio_path):
            prediction = self.model_whisper.transcribe(f"{self.audio_path}")

            # checking only 0 segment - is it possible to get more than one segment?
            if len(prediction["segments"]):
                if prediction["segments"][0]["no_speech_prob"] < self.accepted_prob:
                    predicted_texts = ''.join([prediction["text"]])


        return predicted_texts

    def pause(self):
        self.stream.close()

    def start(self):
        # Open stream using callback (3)
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=self.channels,
                        rate=self.fs,
                        input=True,
                        stream_callback=self.__callback)

    def cleanVoiceFile(self):
        self.frames = np.array([[],[]])
        if platform == "win32" or platform == "win64":
            os.system(f"del {self.audio_path}")


    def close(self):
        # Close stream (4)
        self.stream.close()

        # Release PortAudio system resources (5)
        self.p.terminate()

if __name__ == "__main__":

    v2s = voice2Speech()
    v2s.listen()

    for n in range(100000):
        text = v2s.process()
        print(text)
        time.sleep(0.1)

    v2s.close()
