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

import math
import struct
import time

import matplotlib.pyplot as plt
import numpy as np

from pyNAVIS_functions.loaders import SpikesFile


def checkSpikesFile(spikes_file, settings):
    '''
    Checks if the spiking information contained in the SpikesFile is correct and prints "The loaded SpikesFile file has been checked and it's OK" if the file passes all the checks.
    
    Parameters:
            spikes_file (SpikesFile): file to check.
            settings (MainSettings): configuration parameters for the file to check.

    Returns:
            None.
    
    Raises:
            ValueError: if the SpikesFile contains at least one timestamp which value is less than 0.
            ValueError: if the SpikesFile contains at least one timestamp that is lesser than its previous one.
            ValueError: if the SpikesFile contains at least one address less than 0 or greater than the num_channels that you specified in the MainSettings.
                NOTE: If mono_stereo is set to 1 (stereo) in the MainSettings, then  addresses should be less than num_channels*2
                NOTE: If on_off_both is set to 2 (both) in the MainSettings, then addresses should be less than num_channels*2.
                NOTE: If mono_stereo is set to 1 and on_off_both is set to 2 in the MainSettings, then addresses should be less than num_channels*2*2.
    '''
    if settings.on_of_both == 2:
        number_of_addresses = settings.num_channels*2
    else:
        number_of_addresses = settings.num_channels
    # Check if all timestamps are greater than zero
    a = all(item >= 0  for item in spikes_file.timestamps)

    if not a:
        raise ValueError("The SpikesFile file that you loaded has at least one timestamp that is less than 0.")

    # Check if each timestamp is greater than its previous one
    b = not any(i > 0 and spikes_file.timestamps[i] < spikes_file.timestamps[i-1] for i in range(len(spikes_file.timestamps)))

    if not b:
        raise ValueError("The SpikesFile file that you loaded has at least one timestamp whose value is lesser than its previous one.")

    # Check if all addresses are between zero and the total number of addresses
    c = all(item >= 0 and item < number_of_addresses*(settings.mono_stereo+1) for item in spikes_file.addresses)

    if not c:
        raise ValueError("The SpikesFile file that you loaded has at least one event whose address is either less than 0 or greater than the number of addresses that you specified.")

    if a and b and c:
        print("The loaded SpikesFile file has been checked and it's OK")
            

# 
def adaptAERDATA(spikes_file, settings):
    '''
    Subtracts the smallest timestamp of the SpikesFile to all of the timestamps contained in the file (in order to start from 0)
    It also adapts timestamps based on the tick frequency (ts_tick in the MainSettings).
    
    Parameters:
            spikes_file (SpikesFile): file to adapt.
            settings (MainSettings): configuration parameters for the file to adapt.

    Returns:
            spikes_file (SpikesFile):  adapted SpikesFile.
    '''
    minimum_ts = min(spikes_file.timestamps)
    if settings.reset_timestamp:
        spikes_file.timestamps = [(x - minimum_ts)*settings.ts_tick for x in spikes_file.timestamps]
    else:
        spikes_file.timestamps = [x*settings.ts_tick for x in spikes_file.timestamps]
    return spikes_file


def phaseLock(spikes_file, settings):
    '''
    Performs the phase lock operation over a SpikesFile. This can only be performed to SpikeFiles with both ON and OFF addresses.
    
    Parameters:
            spikes_file (SpikesFile): file used to perform the phase lock.
            settings (MainSettings): configuration parameters of the input file.

    Returns:
            spikes_file (SpikesFile):  phase-locked SpikesFile.

    Raises:
            AttributeError: if the on_of_both parameter is not set to 2 (both) in the MainSettings.
    '''

    if settings.on_off_both == 2:
        prevSpike = [None] * (settings.num_channels) * (1 + settings.mono_stereo)
        phaseLockedAddrs = []
        phaseLockedTs = []
        for i in range(len(spikes_file.addresses)):
            if prevSpike[spikes_file.addresses[i]//2] == None:
                prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
            else:
                if prevSpike[spikes_file.addresses[i]//2] == 0 and spikes_file.addresses[i]%2 == 1:
                    phaseLockedAddrs.append(spikes_file.addresses[i]//2)
                    phaseLockedTs.append(spikes_file.timestamps[i])
                    prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
                else:
                    prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
        spikes_file = SpikesFile()
        spikes_file.addresses = phaseLockedAddrs
        spikes_file.timestamps = phaseLockedTs
        return spikes_file
    else:
        raise AttributeError("Phase Lock: this functionality cannot be applied to files that do not have ON/positive and OFF/negative addresses. Check the on_of_both setting for more information.")


def extract_channels_activities(spikes_file, addresses, verbose = False):
    '''
    Extract information from a specific set of addresses from the SpikesFile.
    
    Parameters:
            spikes_file (SpikesFile): file to use.
            addresses (int[]): list of addresses to extract.
            verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

    Returns:
            new_spikes_file (SpikesFile):  SpikesFile containing only the information from the addresses specified as input from spikes_file.
    '''

    if verbose == True: start_time = time.time()
    spikes_per_channels_ts = []
    spikes_per_channel_addr = []
    for i in range(len(spikes_file.timestamps)):
        if spikes_file.addresses[i] in addresses:
            spikes_per_channels_ts.append(spikes_file.timestamps[i])
            spikes_per_channel_addr.append(spikes_file.addresses[i])
    if verbose == True: print('EXTRACT CHANNELS CALCULATION', time.time() - start_time)
    new_spikes_file = SpikesFile()
    new_spikes_file.addresses = spikes_per_channel_addr
    new_spikes_file.timestamps = spikes_per_channels_ts
    return new_spikes_file


def get_info(spikes_file):
    '''
    Prints the number of spikes and the number of microseconds of audio that the SpikesFile contains.
    
    Parameters:
            spikes_file (SpikesFile): file to get the information from.

    Returns:
            None.
    '''

    print("The file contains", len(spikes_file.addresses), "spikes")
    print("The audio has", max(spikes_file.timestamps), 'microsec')
