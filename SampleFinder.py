
import queue
import threading
from time import sleep
from random import randint
from Globals import PLATEAUYMAX, PLATEAUXMAX

class SampleFinder:

    def __init__(self):
        self.sampleQueue = queue.Queue()
        self.threadForSamples = threading.Thread(target = self.sampleFinderProcess)
        self.threadForSamples.start()


    def sampleFinderProcess(self):
        while True:
            randomSample = (randint(1, PLATEAUXMAX), randint(1, PLATEAUYMAX))
            self.sampleQueue.put(randomSample)
            sleep(randint(1,2))


    def getNextSample(self):
        return self.sampleQueue.get()