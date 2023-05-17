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
        pass

    def dwa(self):
            pass

if __name__ == "__main__":
    # chunk = 1024  # Record in chunks of 1024 samples
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    # fs = 16000  # Record at 44100 samples per second
    # seconds = 3
    tmp_path = "tmp_audio"
    filename = "output.wav"
    fileIterator = 0
    maxFiles = 10
    stop = False

    max_buff_size = fs*10
    frames = np.array([[],[]])

    model_whisper = whisper.load_model("base")
    accepted_prob = 0.5

    predicted_texts = ""


    def callback(in_data, frame_count, time_info, status):
        global frames
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        audio_data = np.array([audio_data[1::2],audio_data[::2]])
        frames = np.append(frames,audio_data,axis=1)
        return (in_data, pyaudio.paContinue)

    # Instantiate PyAudio and initialize PortAudio system resources (2)
    p = pyaudio.PyAudio()

    # Open stream using callback (3)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=channels,
                    rate=fs,
                    input=True,
                    stream_callback=callback)

    for n in range(10):
        audio_path = "tmp_stream.wav"
        tmp_frames = frames.copy()
        frames = np.array([[],[]])

        # Write wav data to the temporary file as bytes.
        sf.write(f"{audio_path}",tmp_frames.T,fs)

        if os.path.exists(audio_path):
            prediction = model_whisper.transcribe(f"{audio_path}")

            # checking only 0 segment - is it possible to get more than one segment?
            if len(prediction["segments"]):
                if prediction["segments"][0]["no_speech_prob"] < accepted_prob:
                    predicted_texts = ''.join([predicted_texts,prediction["text"]])

            if platform == "win32" or platform == "win64":
                os.system(f"del {audio_path}")

            print(predicted_texts)

        time.sleep(1)


    # Close stream (4)
    stream.close()

    # Release PortAudio system resources (5)
    p.terminate()
    pass
