from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.utils import *
from pyNAVIS_functions.raw_audio_functions import *
from pyNAVIS_functions.aedat_functions import *
from pyNAVIS_functions.aedat_splitters import *
from pyNAVIS_settings.main_settings import *


#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\1khz_test_pdm_mono_30att2.aedat'
#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\c120e80e_nohash_8.wav.aedat'
#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\train_cut.aedat'
#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\test.aedat'
path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\00176480_nohash_0.wav.aedat'

settings = MainSettings(p_num_channels=32, p_mono_stereo=0, p_address_size=2, p_ts_tick=0.2, p_bin_size=20000, p_bar_line=1, p_spikegram_dot_freq=10)
#settings = MainSettings(p_num_channels=32, p_mono_stereo=0, p_address_size=2, p_ts_tick=0.2, p_bin_size=20000, p_bar_line=1, p_spikegram_dot_freq=2)


add, ts = loadAERDATA(path, settings)
ts = adaptAERDATA(ts, settings)
checkAERDATA(add, ts, settings)

print "The file contains", len(add), "spikes"
print "The audio has", max(ts), 'microsec'


"""
mean_new = 0
for i in range(it):
    mean_new = mean_new + execution_time(loadAERDATA, [path, settings])
    print 'Iteration', i+1, 'of', it 

print 'Mean time new', mean_new/it
"""

#print execution_time(loadAERDATA, [path, settings])                                             ##0.73
                                                                          #1081113 spikes
print execution_time(spikegram, (add, ts, settings))                        #3.06
print execution_time(sonogram, (add, ts, settings))                         #16.01
print execution_time(histogram, (add, settings))                             #0.7                ##0.04
print execution_time(average_activity,(add, ts, settings))                                      ##0.58
#print execution_time(difference_between_LR, (add, ts, settings))            #15.82


#print execution_time(sonogram_old, (add, ts, settings))
#print execution_time(difference_between_LR_old, (add, ts, settings))


#manual_aedat_splitter(add, ts, 0, max(ts), "a.aedat", settings)
#automatic_aedat_splitter(add, ts, 20, 0.015, settings, "")
raw_input()