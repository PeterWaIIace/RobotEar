from sys import  platform
import time
import whisper
import shutil
import os

class CommandDecoder:

    def __init__(self,tmp_directory):
        self.model_whisper = whisper.load_model("medium")
        self.tmp_path      = tmp_directory
        self.decode_path   = "decode_audio"
        self.accepted_prob = 0.7

    def decode(self):
        self.__cpy_tmp()

        predicted_texts = []

        for audio_path in os.listdir(self.decode_path):
            prediction = self.model_whisper.transcribe(f"{self.decode_path}/{audio_path}")

            # checking only 0 segment - is it possible to get more than one segment?
            if prediction["segments"][0]["no_speech_prob"] < self.accepted_prob:
                predicted_texts.append(prediction["text"])

        self.__clean_tmp()
        return predicted_texts

    def __cpy_tmp(self):
        for f in os.listdir(self.tmp_path):
            source_file = os.path.join(self.tmp_path, f)
            destination_file = os.path.join(self.decode_path, f)
            shutil.copy2(source_file, destination_file)

    def __clean_tmp(self):
        dir_list = os.listdir(self.decode_path)

        for f in dir_list:
            if platform == "win32" or platform == "win64":
                os.system(f"del {self.decode_path}\\{f}")

def decode():

    path = "tmp_audio"
    cmdDec = CommandDecoder(path)
    for _ in range(20):
        print(cmdDec.decode())

if __name__ == "__main__":

    decode()