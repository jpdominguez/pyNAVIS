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

import random

import numpy as np

from .loaders import SpikesFile
from .savers import Savers
from settings.main_settings import MainSettings

class Generators:
    
    @staticmethod
    def sweep(freq, cycles, num_ch, length, path = None, output_format = '.aedat', return_save_both = 0):
        '''
        Generates a SpikesFile with spikes going from address 0 to address N and back, repeating it for a specific number of cycles.
        
            Parameters:
                    freq (int): Number of spikes generated per address and half-cycle.
                    cycles (int): Number of repetitions.
                    num_ch (int): Number of addresses that the sweep will consider.
                    length (int): Number of microseconds that the SpikesFile will have.
                    path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                    output_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.
                    return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.

            Returns:
                    spikes_file (SpikesFile, optional): SpikesFile containing the sweep. Returned only if return_save_both is either 0 or 2.
        '''

        spikes_file = SpikesFile()
        time_per_cycle = float(length) // cycles
        spikes_per_cycle = freq * (num_ch * 2 - 1)
        time_between_spikes = float(time_per_cycle) // spikes_per_cycle

        addrs = [0] * int(spikes_per_cycle*cycles)
        timestamps = [0] * int(spikes_per_cycle*cycles)
        current_spike_id = 0    

        for c in range(cycles):
            for i in range((num_ch*2)-1):
                for j in range(freq):
                    addrs[current_spike_id] = i - (i//num_ch)*(((i%(num_ch))+1)*2)
                    timestamps[current_spike_id] = int(current_spike_id*time_between_spikes)
                    current_spike_id += 1
        settings = MainSettings(num_channels = num_ch, mono_stereo = 0)

        spikes_file.timestamps = timestamps
        spikes_file.addresses = addrs

        if return_save_both == 0:
            return spikes_file
        elif return_save_both == 1 or return_save_both == 2:
            if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
                Savers.save_AERDATA(spikes_file, path + '.aedat', settings)
            elif output_format == 'csv' or 'CSV' or '.csv':
                Savers.save_CSV(spikes_file, path + '.csv', settings)        
            if return_save_both == 2:
                return spikes_file

    @staticmethod
    def shift(freq, num_ch, length, path = None, output_format = '.aedat', return_save_both = 0):
        '''
        Generates a SpikesFile with spikes going from address 0 to address N.
        
            Parameters:
                    freq (int): Number of spikes generated per address.
                    num_ch (int): Number of addresses that the shift will consider.
                    length (int): Number of microseconds that the SpikesFile will have.
                    path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                    output_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.
                    return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.

            Returns:
                    spikes_file (SpikesFile, optional): SpikesFile containing the shift. Returned only if return_save_both is either 0 or 2.
        '''

        spikes_file = SpikesFile()
        total_spikes_no = freq * num_ch
        addrs = [0] * int(total_spikes_no)
        timestamps = [0] * int(total_spikes_no)
        current_spike_id = 0
        
        time_between_spikes = float(length) // total_spikes_no

        for i in range(num_ch):
            for j in range(freq):
                addrs[current_spike_id] = i
                timestamps[current_spike_id] = int(current_spike_id*time_between_spikes)
                current_spike_id += 1
        settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
        spikes_file.timestamps = timestamps
        spikes_file.addresses = addrs
        if return_save_both == 0:
            return spikes_file
        elif return_save_both == 1 or return_save_both == 2:
            if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
                Savers.save_AERDATA(spikes_file, path + '.aedat', settings)
            elif output_format == 'csv' or 'CSV' or '.csv':
                Savers.save_CSV(spikes_file, path + '.csv', settings)        
            if return_save_both == 2:
                return spikes_file

    @staticmethod
    def random_addrs(freq, num_ch, length, path = None, output_format = '.aedat', return_save_both = 0):
        '''
        Generates a SpikesFile with spikes going from address 0 to address N.
        
            Parameters:
                    freq (int): Frequency of the spikes generated per address.
                    num_ch (int): Number of addresses that the process will consider.
                    length (int): Number of microseconds that the SpikesFile will have.
                    path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                    output_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.
                    return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.

            Returns:
                    spikes_file (SpikesFile, optional): SpikesFile containing the spikes. Returned only if return_save_both is either 0 or 2.
        '''

        spikes_file = SpikesFile()
        addrs = [0] * int(freq*length/1000000)
        timestamps = [0] * int(freq*length/1000000)
        random.seed(0)
        for i in range(int(freq*length/1000000)):
            addrs[i] = random.randint(0, num_ch-1)
            timestamps[i] = int(i*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds
        
        settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
        spikes_file.timestamps = timestamps
        spikes_file.addresses = addrs
        if return_save_both == 0:
            return spikes_file
        elif return_save_both == 1 or return_save_both == 2:
            if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
                Savers.save_AERDATA(spikes_file, path + '.aedat', settings)
            elif output_format == 'csv' or 'CSV' or '.csv':
                Savers.save_CSV(spikes_file, path + '.csv', settings)        
            if return_save_both == 2:
                return spikes_file