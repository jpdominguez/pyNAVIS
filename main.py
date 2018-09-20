from pyNAVIS_functions.Screens import *
from pyNAVIS_functions.loadAERDATA import *
from pyNAVIS_functions.utils import *



#import time
#start_time = time.time()
#print "The file took ", time.time() - start_time




#Parameters
path = 'D:\\Repositorios\\GitHub\\loadAERDATA\\c120e80e_nohash_8.wav.aedat'
bin_size = 20000
ts_tick = 0.2
num_channels = 32
mono_stereo = 0 #0-mono, 1-stereo

reset_timestamp = True

spikegram_dot_size = 0.1

bar_line = 1 #0-bar, 1-line



[add, ts] = loadAERDATA(path)
ts = adaptAERDATA(ts, reset_timestamp, ts_tick)
if checkAERDATA(ts, num_channels, add):
    print "The loaded AER-DATA file has been checked and it's OK"

print len(add)
print execution_time(loadAERDATA, [path])
print execution_time(spikegram, (add, ts, spikegram_dot_size))
print execution_time(sonogram, (add, ts, num_channels, bin_size))
print execution_time(histogram, (add, num_channels, mono_stereo, bar_line))
print execution_time(average_activity,(ts, bin_size))

"""
sonogram(add, ts, num_channels, bin_size)
histogram(add, num_channels, mono_stereo, bar_line)
average_activity(ts, bin_size)
raw_input()
"""