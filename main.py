from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.utils import *
from pyNAVIS_functions.raw_audio_functions import *
from pyNAVIS_functions.aedat_functions import *
from pyNAVIS_functions.aedat_splitters import *
from pyNAVIS_settings.main_settings import *

path = 'D:\\Repositorios\\GitHub\\pyNAVIS\\aedats\\CochleaAMS1c-2018-10-10T09-49-41+0200-ARIOS01X-0.aedat'

settings = MainSettings(p_num_channels=32, p_mono_stereo=0, p_address_size=4, p_ts_tick=1, p_bin_size=20000, p_bar_line=1, p_spikegram_dot_freq=5)

add, ts = loadAERDATA(path, settings)
ts = adaptAERDATA(ts, settings)
checkAERDATA(add, ts, settings)

print "The file contains", len(add), "spikes"
print "The audio has", max(ts), 'microsec'


print execution_time(spikegram, (add, ts, settings))
print execution_time(sonogram, (add, ts, settings))
print execution_time(histogram, (add, settings))
print execution_time(average_activity,(add, ts, settings))
#print execution_time(difference_between_LR, (add, ts, settings))
#manual_aedat_splitter(add, ts, 0, max(ts), "a.aedat", settings)

raw_input()