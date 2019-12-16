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
from pyNAVIS_functions.dataset_gen import generate_sonogram_dataset
from pyNAVIS_functions.loaders import *                                                  #
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

spikes_file = loadAERDATA('0a2b400e_nohash_0.wav.aedat', settings)
spikes_file = adaptAERDATA(spikes_file, settings)
checkAERDATA(spikes_file, settings)
get_info(spikes_file)
spikegram(spikes_file, settings, graph_tile='Original aedat', verbose=True)
#sonogram(spikes_file, settings, verbose=True)
#histogram(spikes_file, settings, verbose=True)
#average_activity(spikes_file, settings, verbose=True)
#difference_between_LR(spikes_file, settings, verbose=True)     #NEEDS TEST
#save_AERDATA(spikes_file, "hey.aedat", settings,verbose=True)
#save_CSV(spikes_file, "hey.csv", verbose=True)
#save_TXT(spikes_file, "heyTxt.txt", verbose=True)
#save_TXT_relativeTS(spikes_file, "heyTXTrelative", verbose=True)
#monoToStereo(spikes_file, 0, "stereo.aedat", settings)


phaseLocked_spikes = phaseLock(spikes_file, settings)
get_info(phaseLocked_spikes)
settings = MainSettings(num_channels=num_channels, on_off_both=1, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
spikegram(phaseLocked_spikes, settings, graph_tile='phaseLock', verbose=True)
#sonogram(phaseLocked_spikes, settings, verbose=True)
#histogram(phaseLocked_spikes, settings, verbose=True)
#average_activity(phaseLocked_spikes, settings, verbose=True)
#save_AERDATA(phaseLocked_spikes, "hey.aedat", settings,verbose=True)
#save_CSV(phaseLocked_spikes, "hey.csv", verbose=True)
#save_TXT(phaseLocked_spikes, "heyTxt.txt", verbose=True)
#save_TXT_relativeTS(phaseLocked_spikes, "heyTXTrelative", verbose=True)
monoToStereo(phaseLocked_spikes, 0, "stereoPS.aedat", settings)


prueba = extract_channels_activities(phaseLocked_spikes, range(0, 16), verbose=True)
spikegram(prueba, settings, graph_tile='phaseLock spikes extract addresses', verbose=False)


settings = MainSettings(num_channels=32, on_off_both=1, mono_stereo=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
spikes_file = loadAERDATA('stereoPS.aedat', settings)
spikes_file = adaptAERDATA(spikes_file, settings)
checkAERDATA(spikes_file, settings)
get_info(spikes_file)
spikegram(spikes_file, settings, graph_tile='phaselock monoToStereo', verbose=True)
difference_between_LR(spikes_file, settings, verbose=True)


"""
settings = MainSettings(num_channels=32, mono_stereo=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
spikes_file = loadAERDATA('stereo.aedat', settings)
spikes_file = adaptAERDATA(spikes_file, settings)
checkAERDATA(spikes_file, settings)
get_info(spikes_file)
spikegram(spikes_file, settings, verbose=True)
"""

plt.show()
#save_CSV(add, ts, 'C:\\Users\\juado\\Desktop\\en_un_mono_left')
#save_TXT(add, ts, 'C:\\Users\\juado\\Desktop\\en_un_mono_left')

#manual_aedat_splitter(add, ts, 0, max(ts), "a.aedat", settings)

#stereoToMono(add, ts, 0, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_left.aedat', settings)
#stereoToMono(add, ts, 1, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_right.aedat', settings)
#raw_input()
