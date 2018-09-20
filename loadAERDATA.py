import struct
import numpy as np
import matplotlib.pyplot as plt
import math

from pyNAVIS_functions.Screens import *
from pyNAVIS_functions.loadAERDATA import *
from pyNAVIS_functions.utils import *


path = 'D:\\Repositorios\\GitHub\\loadAERDATA\\c120e80e_nohash_8.wav.aedat'

#import time
#start_time = time.time()
[add, ts] = loadAERDATA(path)
#print "The file took ", time.time() - start_time

ts = adaptAERDATA(ts, True, 0.2)

if checkAERDATA(ts, 64, add):
    print "The loaded AER-DATA file has been checked and it's OK"

spikegram(add, ts, 0.1)
sonogram(add, ts, 32, 20000)
histogram(add, 32, 0, 1)
average_activity(ts, 20000)

raw_input()