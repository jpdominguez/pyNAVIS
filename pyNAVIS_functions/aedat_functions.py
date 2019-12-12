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

import struct
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from pyNAVIS_functions.loaders import SpikesFile

def checkAERDATA(spikes_file, settings):

    number_of_addresses = settings.num_channels*2
    # Check if all timestamps are greater than zero
    a = all(item >= 0  for item in spikes_file.timestamps)

    if not a:
        print("The AER-DATA file that you loaded has at least one timestamp that is below 0.")

    # Check if each timestamp is greater than its previous one
    b = not any(i > 0 and spikes_file.timestamps[i] < spikes_file.timestamps[i-1] for i in range(len(spikes_file.timestamps)))

    if not b:
        print("The AER-DATA file that you loaded has at least one timestamp whose value is lesser than its previous one.")

    # Check if all addresses are between zero and the total number of addresses
    c = all(item >= 0 and item < number_of_addresses*(settings.mono_stereo+1) for item in spikes_file.addresses)

    if not c:
        print("The AER-DATA file that you loaded has at least one event whose address is either below 0 or above the number of addresses that you specified.")

    if a and b and c:
        print("The loaded AER-DATA file has been checked and it's OK")
            

# Function to subtract the smallest timestamp to all of the events (to start from 0) and adapt them based on the tick frequency of the tool used to log the file.
def adaptAERDATA(spikes_file, settings):
    minimum_ts = min(spikes_file.timestamps)
    if settings.reset_timestamp:
        spikes_file.timestamps = [(x - minimum_ts)*settings.ts_tick for x in spikes_file.timestamps]
    else:
        spikes_file.timestamps = [x*settings.ts_tick for x in spikes_file.timestamps]
    return spikes_file


def phaseLock(spikes_file, settings):
    prevSpike = [None] * (settings.num_channels) * (1 + settings.mono_stereo)
    phaseLockedAddrs = []
    phaseLockedTs = []
    for i in range(len(spikes_file.addresses)):
        if prevSpike[spikes_file.addresses[i]//2] == None:
            prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
        else:
            if prevSpike[spikes_file.addresses[i]//2] == 0 and spikes_file.addresses[i]%2 == 1:
                phaseLockedAddrs.append(spikes_file.addresses[i]/2)
                phaseLockedTs.append(spikes_file.timestamps[i])
                prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
            else:
                prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
    spikes_file = SpikesFile()
    spikes_file.addresses = phaseLockedAddrs
    spikes_file.timestamps = phaseLockedTs
    return spikes_file


def extract_channels_activities(spikes_file, channels):
    spikes_per_channels_ts = []
    spikes_per_channel_addr = []
    for i in range(len(spikes_file.timestamps)):
        if spikes_file.addresses[i] in channels:
            spikes_per_channels_ts.append(spikes_file.timestamps[i])
            spikes_per_channel_addr.append(spikes_file.addresses[i])
    return spikes_per_channel_addr, spikes_per_channels_ts


def get_info(spikes_file):
    print("The file contains", len(spikes_file.addresses), "spikes")
    print("The audio has", max(spikes_file.timestamps), 'microsec')