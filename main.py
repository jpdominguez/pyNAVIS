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
#############################################################################################################################

## PARAMETERS ###############################################################################################################
num_channels = 2      # Number of NAS channels (not addresses but channels).                                               #
mono_stereo = 0        # 0 for a monaural NAS or 1 for a binaural NAS.                                                      #
address_size = 2       # 2 if .aedats are recorded with USBAERmini2 or 4 if .aedats are recorded with jAER.                 #
ts_tick = 0.2            # 0.2 if .aedats are recorded with USBAERmini2 or 1 if .aedats are recorded with jAER.               #
bin_size = 20000       # Time bin (in microseconds) used to integrate the spiking information.                              #
bar_line = 1           # 0 if you want the histogram to be a bar plot or 1 if you want the histogram to be a line plot.     #
spike_dot_freq = 1     # When plotting the cochleogram, it plots one spike for every spike_dot_frPeq spikes.                #
#############################################################################################################################


#random_addrs(freq=100000, num_ch=10, length=2, path='C:\\Users\\juado\\Desktop\\en_un_mono_left.aedat')
sweep(freq=80, cycles=2, num_ch=4, length=5000, path='C:\\Users\\juado\\Desktop\\en_un_mono_left.aedat')


path = 'C:\\Users\\juado\\Desktop\\en_un_mono_left.aedat'

settings = MainSettings(num_channels=num_channels, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq)

add, ts = loadAERDATA(path, settings)
ts = adaptAERDATA(ts, settings)
checkAERDATA(add, ts, settings)

#print "The file contains", len(add), "spikes"
#print "The audio has", max(ts), 'microsec'


print execution_time(spikegram, (add, ts, settings))
print execution_time(sonogram, (add, ts, settings))
print execution_time(histogram, (add, settings))
#print execution_time(average_activity,(add, ts, settings))
#print execution_time(difference_between_LR, (add, ts, settings))

#manual_aedat_splitter(add, ts, 0, max(ts), "a.aedat", settings)

#stereoToMono(add, ts, 0, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_left.aedat', settings)
#stereoToMono(add, ts, 1, 'C:\\Users\\jpdominguez\\Desktop\\en_un_mono_right.aedat', settings)
raw_input()

