__author__ = 'Fabian'
from multiprocessing import cpu_count

BASIC = 0
FREQSWEEP = 1
methods = BASIC, FREQSWEEP

class Settings:
    methods = len(methods)
    def __init__(self, testtime = 60, frequency = 2.0, method = BASIC, cpucount = cpu_count()):
        self.testtime = testtime
        self.frequency = frequency
        self.frequency2 = 2
        self.cpucount = cpucount
        self.method = method
