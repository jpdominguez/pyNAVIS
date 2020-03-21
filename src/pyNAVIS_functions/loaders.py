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


class SpikesFile:
    """
    Class with all the addresses and timestamps of a file.

    Attributes:
        timestamps (int[]): timestamps of the file.
        addresses (int[]): addresses of the file.
        NOTE: timestamps and addresses are matches, which means that timestamps[0] is the timestamp for the spike with address addresses[0].
    """
    timestamps = []
    addresses = []


def loadAERDATA(path, settings):
    '''
    Loads an AER-DATA (.aedat) file.
    
        Parameters:
                path (string): full path of the AER-DATA file to be loaded, including name and extension.
                settings (MainSettings): configuration parameters for the file to load.

        Returns:
                spikes_file (SpikesFile): SpikesFile containing all the addresses and timestamps of the file.
    '''
    unpack_param = ">H"
    
    if settings.address_size == 2:
        unpack_param = ">H"
    elif settings.address_size == 4:
        unpack_param = ">L"
    else:
        print("Only address sizes implemented are 2 and 4 bytes")

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
    spikes_file = SpikesFile()
    spikes_file.addresses = events
    spikes_file.timestamps = timestamps
    return spikes_file
