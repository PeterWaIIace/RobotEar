from commandDecoder import CommandDecoder
from voiceRecorder import CommandRecorder
import time
import multiprocessing


def decode():

    path = "tmp_audio"
    cmdDec = CommandDecoder(path)
    for _ in range(1000):
        print(cmdDec.decode())
        time.sleep(1)

    print("finished")

if __name__ == "__main__":
    cmdRec = CommandRecorder()

    p = multiprocessing.Process(target=decode)
    p.start()
    time.sleep(10)

    cmdRec.record()

    for n in range(10):
        print(n)
        time.sleep(10)

    cmdRec.close()
    p.join()
    print("stop")
