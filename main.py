from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.loadAERDATA import *
from pyNAVIS_functions.utils import *
from pyNAVIS_functions.raw_audio_functions import *
from pyNAVIS_settings.main_settings import *


#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\1khz_test_pdm_mono_30att2.aedat'
#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\c120e80e_nohash_8.wav.aedat'
#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\train_cut.aedat'
path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\test.aedat'

settings = MainSettings(p_num_channels=64, p_mono_stereo=1, p_address_size=4, p_ts_tick=0.1, p_bin_size=2000, p_bar_line=1, p_spikegram_dot_freq=100)
#settings = MainSettings(p_num_channels=32, p_mono_stereo=0, p_address_size=2, p_ts_tick=0.2, p_bin_size=20000, p_bar_line=1, p_spikegram_dot_freq=2)


add, ts = loadAERDATA(path, settings)
ts = adaptAERDATA(ts, settings)
checkAERDATA(add, ts, settings)

print "The file contains", len(add), "spikes"
print "The audio has", max(ts), 'microsec'


"""
mean_new = 0
mean_new_true = 0
mean_old = 0
it = 10
for i in range(it):
    mean_new = mean_new + execution_time(loadAERDATA, [path, settings])
    mean_new_true = mean_new_true + execution_time(loadAERDATA_true, [path, settings])
    #mean_old = mean_old + execution_time(loadAERDATA_old, [path, settings])
    print 'Iteration', i+1, 'of', it 

print 'Mean time new', mean_new/it
print 'Mean time new TRUE', mean_new_true/it
"""
#print 'Mean time old', mean_old/it

for i in range(10):
    print '1:', execution_time(loadAERDATA, [path, settings])

#print execution_time(loadAERDATA, [path, settings])                         #2.8  #2.15
#print execution_time(loadAERDATA_old, [path, settings])
                                                                            #928617 spikes
#print execution_time(spikegram, (add, ts, settings))                        #3.06
#print execution_time(sonogram, (add, ts, settings))                         #16.01
#print execution_time(histogram, (add, settings))                            #0.7
#print execution_time(average_activity,(add, ts, settings))                  #27.0  #17.15 #0.84
#print execution_time(difference_between_LR, (add, ts, settings))            #15.82

raw_input()