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

#from src import *


from pyNAVIS import *

import matplotlib.pyplot as plt
#############################################################################################################################

## PARAMETERS ###############################################################################################################
num_channels = 32      # Number of NAS channels (not addresses but channels).                                               #
mono_stereo = 0        # 0 for a monaural NAS or 1 for a binaural NAS.                                                      #
address_size = 2       # 2 if .aedats are recorded with USBAERmini2 or 4 if .aedats are recorded with jAER.                 #
ts_tick = 0.2          # 0.2 if .aedats are recorded with USBAERmini2 or 1 if .aedats are recorded with jAER.               #
bin_size = 20000       # Time bin (in microseconds) used to integrate the spiking information.                              #
#############################################################################################################################

path = 'C:\\Users\\juado\\Desktop'

# TEST GENERATORS

#NOTE: Sweep
sweep_spikes = Generators.sweep(freq=5, cycles=5, num_ch=64, length=1000000, path='C:\\Users\\juado\\Desktop\\sweep', return_save_both=0)
sweep_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
Plots.spikegram(sweep_spikes, sweep_settings)
#Plots.sonogram(sweep_spikes, sweep_settings)
#Plots.histogram(sweep_spikes, sweep_settings)
#Plots.average_activity(sweep_spikes, sweep_settings)
"""
#NOTE: Random addresses
random_spikes = Generators.random_addrs(freq=5400, num_ch=64, length=1000000, path='C:\\Users\\juado\\Desktop\\sweep', return_save_both=0)
random_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
Plots.spikegram(random_spikes, random_settings)
Plots.sonogram(random_spikes, random_settings)
Plots.histogram(random_spikes, random_settings)
Plots.average_activity(random_spikes, sweep_settings)

#NOTE: Shift
shift_spikes = Generators.shift(freq=100, num_ch=64, length=1000000, path='C:\\Users\\juado\\Desktop\\shift', return_save_both=0)
shift_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
Plots.spikegram(shift_spikes, shift_settings)
Plots.sonogram(shift_spikes, shift_settings)
Plots.histogram(shift_spikes, shift_settings)
Plots.average_activity(shift_spikes, shift_settings)
"""


"""
#NOTE: Loading a stereo file
settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
stereo_file = Loaders.loadAERDATA('D:\\Repositorios\\GitHub\\pyNAVIS\\src\\stereoPS.aedat', settings)
stereo_file = Functions.adapt_SpikesFile(stereo_file, settings)
#Functions.check_SpikesFile(stereo_file, settings)
Plots.spikegram(stereo_file, settings)
#Plots.sonogram(stereo_file, settings)
#Plots.histogram(stereo_file, settings)
#Plots.average_activity(stereo_file, settings)
#Plots.difference_between_LR(stereo_file, settings)
"""
"""
#NOTE: Manual split over a stereo file
manual_split_spikes = Splitters.manual_splitter(stereo_file, init=0, end=100000, settings=settings, return_save_both=0 )
Plots.spikegram(manual_split_spikes, settings, graph_tile='Splitted SpikesFile', verbose=True)
Plots.sonogram(manual_split_spikes, settings, verbose=True)
"""
"""
#NOTE: Test Phaselock
stereo_file = Utils.order_timestamps(stereo_file)
phaseLocked_spikes = Functions.phase_lock(stereo_file, settings)
settings = MainSettings(num_channels=16, on_off_both=0, mono_stereo=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
Plots.spikegram(phaseLocked_spikes, settings, graph_tile='phaseLock', verbose=True)
"""
"""
#NOTE: Test stereo_to_mono
Functions.stereo_to_mono(stereo_file, 1, 'C:\\Users\\juado\\Desktop\\stereoToMono.aedat', settings)
settings = MainSettings(num_channels=16, mono_stereo=0, on_off_both=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
stereo_file = Loaders.loadAERDATA('C:\\Users\\juado\\Desktop\\stereoToMono.aedat', settings)
stereo_file = Functions.adapt_SpikesFile(stereo_file, settings)
Plots.spikegram(stereo_file, settings)
"""

"""
#NOTE: Loading a mono file
settings = MainSettings(num_channels=32, mono_stereo=0, on_off_both=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
mono_file = Loaders.loadAERDATA('D:\\Repositorios\\GitHub\\pyNAVIS\\src\\0a2b400e_nohash_0.wav.aedat', settings)
mono_file = Functions.adapt_SpikesFile(mono_file, settings)
Functions.check_SpikesFile(mono_file, settings)
Plots.spikegram(mono_file, settings)
#Plots.sonogram(mono_file, settings)
#Plots.histogram(mono_file, settings)
#Plots.average_activity(mono_file, settings)
"""
"""
#NOTE: Manual split over a mono file
manual_split_spikes = Splitters.manual_splitter(mono_file, init=0, end=300000, settings=settings, return_save_both=0 )
Plots.spikegram(manual_split_spikes, settings, graph_tile='Splitted SpikesFile', verbose=True)
Plots.sonogram(manual_split_spikes, settings, verbose=True)
"""
"""
#NOTE: Test mono_to_stereo
mono_file = Functions.mono_to_stereo(mono_file, -100000, settings, path='C:\\Users\\juado\\Desktop\\monoToStereo.aedat', return_save_both=0)
settings = MainSettings(num_channels=32, mono_stereo=1, on_off_both=1, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)
#mono_file = Loaders.loadAERDATA('C:\\Users\\juado\\Desktop\\monoToStereo.aedat', settings)
#mono_file = Functions.adapt_SpikesFile(mono_file, settings)
Plots.spikegram(mono_file, settings)
Plots.difference_between_LR(mono_file, settings, return_data=False)
"""

"""
a = Loaders.loadCSV('D:\\Repositorios\\GitHub\\pyNAVIS\\src\\test.csv')

print(a.addresses)
print(a.timestamps)
"""
plt.show()