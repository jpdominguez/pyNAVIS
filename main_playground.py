#################################################################################
##                                                                             ##
##    Copyright C 2018  Juan P. Dominguez-Morales                              ##
##                                                                             ##
##    This file is part of pyNAVIS.                                            ##
##                                                                             ##
##    pyNAVIS is free software: you can redistribute it and/or modify          ##
##    it under the terms of the GNU General Public License as published by     ##
##    the Free Software Foundation, either version 3 of the License, or        ##
##    (at your option) any later version.                                      ##
##                                                                             ##
##    pyNAVIS is distributed in the hope that it will be useful,               ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the              ##
##    GNU General Public License for more details.                             ##
##                                                                             ##
##    You should have received a copy of the GNU General Public License        ##
##    along with pyNAVIS.  If not, see <http://www.gnu.org/licenses/>.         ##
##                                                                             ##
#################################################################################

## IMPORTS ##################################################################################################################
from pyNAVIS_functions.screens_plot import *                                                                                #
from pyNAVIS_functions.utils import *                                                                                       #
from pyNAVIS_functions.raw_audio_functions import *                                                                         #
from pyNAVIS_functions.aedat_functions import *                                                                             #
from pyNAVIS_functions.aedat_splitters import *                                                                             #
from pyNAVIS_settings.main_settings import *                                                                                #
from pyNAVIS_functions.aedat_generators import *                                                                            #
from pyNAVIS_functions.dataset_gen import generate_sonogram_dataset                                                         #
#############################################################################################################################

## PARAMETERS ###############################################################################################################
num_channels = 32      # Number of NAS channels (not addresses but channels).                                               #
mono_stereo = 0        # 0 for a monaural NAS or 1 for a binaural NAS.                                                      #
address_size = 2       # 2 if .aedats are recorded with USBAERmini2 or 4 if .aedats are recorded with jAER.                 #
ts_tick = 0.2          # 0.2 if .aedats are recorded with USBAERmini2 or 1 if .aedats are recorded with jAER.               #
bin_size = 20000       # Time bin (in microseconds) used to integrate the spiking information.                              #
bar_line = 1           # 0 if you want the histogram to be a bar plot or 1 if you want the histogram to be a line plot.     #
spike_dot_freq = 1     # When plotting the cochleogram, it plots one spike for every spike_dot_frPeq spikes.                #
spike_dot_size = 1     # Size of the dots that are plotted on the spikegram                                                 #
#############################################################################################################################


#random_addrs(freq=100, num_ch=64, length=2, path='C:\\Users\\juado\\Desktop\\en_un_mono_left.aedat')
#sweep(freq=80, cycles=4, num_ch=64, length=1000000, path='C:\\Users\\juado\\Desktop\\en_un_mono_left', output_format='aedat')
#shift(freq=10, num_ch=64, length=1000000, path='C:\\Users\\juado\\Desktop\\en_un_mono_left.aedat', output_format='aedat')





path = 'C:\\Users\\juado\\Desktop'

settings = MainSettings(num_channels=num_channels, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)

#generate_sonogram_dataset(path, "C:\\Users\\juado\\Desktop\\test", settings, verbose=True)

add, ts = loadAERDATA('0a2b400e_nohash_0.wav.aedat', settings)
ts = adaptAERDATA(ts, settings)
checkAERDATA(add, ts, settings)
get_info(add, ts)
spikegram(add, ts, settings, verbose=True)


psAddrs, psTs = phaseLock(add, ts, settings)
get_info(psAddrs, psTs)
settings = MainSettings(num_channels=num_channels/2, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
spikegram(psAddrs, psTs, settings, verbose=True)




#save_CSV(add, ts, 'C:\\Users\\juado\\Desktop\\en_un_mono_left')
#save_TXT(add, ts, 'C:\\Users\\juado\\Desktop\\en_un_mono_left')

#manual_aedat_splitter(add, ts, 0, max(ts), "a.aedat", settings)

#stereoToMono(add, ts, 0, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_left.aedat', settings)
#stereoToMono(add, ts, 1, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_right.aedat', settings)
raw_input()

