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
import csv


class SpikesFile:
    """
    Class that contains all the addresses and timestamps of a file.

    Attributes:
            timestamps (int[]): Timestamps of the file.
            addresses (int[]): Addresses of the file.
    Note:
            Timestamps and addresses are matched, which means that timestamps[0] is the timestamp for the spike with address addresses[0].
    """

    def __init__(self, addresses = [], timestamps = []):
        self.addresses = addresses
        self.timestamps = timestamps

class Loaders:
    """
    Functionalities for loading spiking information from different formats.
    """

    @staticmethod
    def loadAEDAT(path, settings):
        """
        Loads an AEDAT (.aedat) file.
        
        Parameters:
                path (string): Full path of the AEDAT file to be loaded, including name and extension.
                settings (MainSettings): Configuration parameters for the file to load.

        Returns:
                SpikesFile: SpikesFile containing all the addresses and timestamps of the file.
        Raises:
                SettingsError: If settings.address_size is different than 2 and 4.

        """
        unpack_param = ">H"
        
        if settings.address_size == 2:
            unpack_param = ">H"
        elif settings.address_size == 4:
            unpack_param = ">L"
        else:
            print("[Loaders.loadAEDAT] > SettingsError: Only address sizes implemented are 2 and 4 bytes")

        with open(path, 'rb') as f:
            ## Check header ##
            p = 0
            lt = f.readline()
            while lt and lt[0] == ord("#"):
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
        spikes_file = SpikesFile([], [])
        spikes_file.addresses = events
        spikes_file.timestamps = timestamps
        return spikes_file


    @staticmethod
    def loadCSV(path):
        """
        Loads a Comma-Separated Values (.csv) file.
        
        Parameters:
                path (string): Full path of the CSV file to be loaded, including name and extension.

        Returns:
                SpikesFile: SpikesFile containing all the addresses and timestamps of the file.

        """
        addresses = []
        timestamps = []
        

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                addresses.append(int(row[0]))
                timestamps.append(int(row[1]))

        spikes_file = SpikesFile([], [])
        spikes_file.addresses = addresses
        spikes_file.timestamps = timestamps
        return spikes_file
