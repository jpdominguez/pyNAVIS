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

def checkAERDATA(allAddr, allTs, settings):

    number_of_addresses = settings.num_channels*2
    # Check if all timestamps are greater than zero
    a = all(item >= 0  for item in allTs)

    if not a:
        print "The AER-DATA file that you loaded has at least one timestamp that is below 0."

    # Check if each timestamp is greater than its previous one
    b = not any(i > 0 and allTs[i] < allTs[i-1] for i in range(len(allTs)))

    if not b:
        print "The AER-DATA file that you loaded has at least one timestamp whose value is lesser than its previous one."

    # Check if all addresses are between zero and the total number of addresses
    c = all(item >= 0 and item < number_of_addresses*(settings.mono_stereo+1) for item in allAddr)

    if not c:
        print "The AER-DATA file that you loaded has at least one event whose address is either below 0 or above the number of addresses that you specified."

    if a and b and c:
        print "The loaded AER-DATA file has been checked and it's OK"
            

# Function to subtract the smallest timestamp to all of the events (to start from 0) and adapt them based on the tick frequency of the tool used to log the file.
def adaptAERDATA(allTs, settings):
    minimum_ts = min(allTs)
    if settings.reset_timestamp:
        return [(x - minimum_ts)*settings.ts_tick for x in allTs]
    else:
        return [x*settings.ts_tick for x in allTs]


def loadAERDATA(path, settings):
    unpack_param = ">H"
    
    if settings.address_size == 2:
        unpack_param = ">H"
    elif settings.address_size == 4:
        unpack_param = ">L"
    else:
        print "Only address sizes implemented are 2 and 4 bytes"

    with open(path, 'rb') as f:
        ## Check header ##
        p = 0
        lt = f.readline()
        while lt and lt[0] == "#":
            p += len(lt)
            lt = f.readline()
        f.seek(p)

        f.seek(0, 2)
        eof = f.tell()

        num_events = math.floor((eof-p)/(settings.address_size + 4))

        f.seek(p)

        events = [0] * int(num_events)
        timestamps = [0] * int(num_events)

        ## Read file ##
        i = 0
        try:
            while 1:
                buff = f.read(settings.address_size)                
                x = struct.unpack(unpack_param, buff)[0]
                events[i] = x

                buff = f.read(4)
                x = struct.unpack('>L', buff)[0]
                timestamps[i] = x

                i += 1
        except Exception as inst:
            pass
    return events, timestamps


def phaseLock(allAddr, allTs, settings):
    prevSpike = [None] * (settings.num_channels) * (1 + settings.mono_stereo)
    #print (settings.num_channels/2) * (1 + settings.mono_stereo)
    #print prevSpike
    phaseLockedAddrs = []
    phaseLockedTs = []
    for i in range(len(allAddr)):
        #print "spike addr", allAddr[i]/2
        if prevSpike[allAddr[i]/2] == None:            
            prevSpike[allAddr[i]/2] = allAddr[i]%2
        else:
            if prevSpike[allAddr[i]/2] == 0 and allAddr[i]%2 == 1:
                phaseLockedAddrs.append(allAddr[i]/2)
                phaseLockedTs.append(allTs[i])
                prevSpike[allAddr[i]/2] = allAddr[i]%2
            else:
                prevSpike[allAddr[i]/2] = allAddr[i]%2

    return phaseLockedAddrs, phaseLockedTs


def get_info(allAddrs, allTs):
    print "The file contains", len(allAddrs), "spikes"
    print "The audio has", max(allTs), 'microsec'