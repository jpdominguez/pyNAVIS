from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.loadAERDATA import *
from pyNAVIS_functions.utils import *
from pyNAVIS_functions.raw_audio_functions import *
from pyNAVIS_settings.main_settings import *


#path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\1khz_test_pdm_mono_30att2.aedat'
path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\c120e80e_nohash_8.wav.aedat'


settings = MainSettings(p_num_channels=32, p_mono_stereo=0, p_address_size=2, p_ts_tick=0.2, p_bin_size=20000)


add, ts = loadAERDATA(path, settings.address_size)
ts = adaptAERDATA(ts, settings.reset_timestamp, settings.ts_tick)
checkAERDATA(ts, settings.num_channels, add)

print "The file contains", len(add), "spikes"


#print execution_time(loadAERDATA, [path])
print execution_time(spikegram, (add, ts, settings.spikegram_dot_size))
"""
print execution_time(sonogram, (add, ts, num_channels, bin_size))
print execution_time(histogram, (add, num_channels, mono_stereo, bar_line))
print execution_time(average_activity,(ts, bin_size))
"""



"""
wav_data, wav_fs = wav_loadWAV('D:\\Repositorios\\GitHub\\pyNAVIS\\c120e80e_nohash_8.wav')
wav_plot(wav_data, wav_fs)
wav_spectrogram(wav_data, wav_fs)
"""


raw_input()