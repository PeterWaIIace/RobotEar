from threading import Thread
from queue import Queue

import pyaudio
import wave
# import OS module
import time
import os

from sys import platform

class commandRecorder:

    def __init__(self):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.seconds = 3
        self.tmp_path = "tmp_audio"
        self.filename = "output.wav"
        self.fileIterator = 0
        self.maxFiles = 10
        self.stop = False

        self.comm_queue = Queue()

        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio

        # clean tmp directory
        self.__clean_tmp()

        self.stream = self.p.open(format=self.sample_format,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)

        print('Recording')

        pass

    def __record(self):
        print(self)
        while not self.stop:
            print(f"__record {self.stop}")

            frames = []  # Initialize array to store frames

            # Store data in chunks for 3 seconds
            for i in range(0, int(self.fs / self.chunk * self.seconds)):
                data = self.stream.read(self.chunk)
                frames.append(data)

            print("send")
            self.comm_queue.put(frames)

    def __save(self):
        while not self.stop:
            if self.comm_queue.qsize() > 0:
                self.filename = f"{self.tmp_path}\\tmp_output_{self.fileIterator}.wav"

                print(f"saving {self.filename} q size = {self.comm_queue.qsize()}")
                frames = self.comm_queue.get()
                wf = wave.open(self.filename, 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.sample_format))
                wf.setframerate(self.fs)
                wf.writeframes(b''.join(frames))
                wf.close()

                self.fileIterator+=1
                self.fileIterator%=self.maxFiles

                if not self.fileIterator:
                    self.__clean_tmp()


    def record(self):

        self.tRecord = Thread(target=self.__record)
        self.tSave   = Thread(target=self.__save)

        self.tRecord.start()
        self.tSave.start()


    def __clean_tmp(self):
        dir_list = os.listdir(self.tmp_path)

        for f in dir_list:
            if platform == "win32" or platform == "win64":
                os.system(f"del {self.tmp_path}\\{f}")
                print(f"removing {f}")

    def close(self):
        self.stop = True

        self.tRecord.join()
        self.tSave.join()

        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()

        # Terminate the PortAudio interface
        self.p.terminate()

        self.__clean_tmp()


if __name__ == "__main__":

    cmdRec = commandRecorder()

    cmdRec.record()

    time.sleep(100)
    cmdRec.close()
