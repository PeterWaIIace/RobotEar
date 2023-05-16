from threading import Thread
from queue import Queue

import sounddevice as sd
import soundfile as sf
import os

from sys import platform

class CommandRecorder:

    def __init__(self):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.seconds = 3
        self.tmp_path = "tmp_audio"
        self.filename = "output.wav"
        self.fileIterator = 0
        self.maxFiles = 10
        self.stop = False

        self.comm_queue = Queue()  # Create an interface to PortAudio

        # clean tmp directory
        self.__clean_tmp()

        print('Recording')

        pass

    def __record(self):
        while not self.stop:

            myrecording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=self.channels, blocking=True)
            self.comm_queue.put(myrecording)


    def __save(self):
        while not self.stop:
            if self.comm_queue.qsize() > 0:
                self.filename = f"{self.tmp_path}\\tmp_output_{self.fileIterator}.wav"

                myRecording = self.comm_queue.get()
                sf.write(self.filename, myRecording, self.fs)

                self.fileIterator+=1
                self.fileIterator%=self.maxFiles

                if not self.fileIterator:
                    self.__clean_tmp()


    def record(self):
        self.stop = False

        # clean tmp directory
        self.__clean_tmp()

        print("start recording")
        self.tRecord = Thread(target=self.__record)
        self.tSave   = Thread(target=self.__save)

        self.tRecord.start()
        self.tSave.start()


    def __clean_tmp(self):
        dir_list = os.listdir(self.tmp_path)

        for f in dir_list:
            if platform == "win32" or platform == "win64":
                os.system(f"del {self.tmp_path}\\{f}")

    def close(self):
        self.stop = True

        self.tRecord.join()
        self.tSave.join()

        # Stop and close the stream
        # self.stream.stop_stream()
        # self.stream.close()

        # Terminate the PortAudio interface
        # self.p.terminate()
        print("closed")

        # self.__clean_tmp()

    def __del__(self):
        self.close()