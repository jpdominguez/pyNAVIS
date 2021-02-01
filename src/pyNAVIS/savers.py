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
import time
from .utils import Utils

class Savers:

    @staticmethod
    def save_AEDAT(spikes_file, path, settings, verbose = False):
        """
        Saves a SpikesFile into an AEDAT file.

        Parameters:
                spikes_file (SpikesFile): File to save.
                path (string): Path where the output file will be saved, including name. Extension should not be specified.
                settings (MainSettings): Configuration parameters for the file to save.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        if verbose == True: start_time = time.time()
        unpack_param = '>L'
        if settings.address_size == 2:
            unpack_param = ">H"
        elif settings.address_size == 4:
            unpack_param = ">L"

        with open(path + '.aedat', 'wb') as f:
            for i in range(len(spikes_file.addresses)):
                addr = struct.pack(unpack_param, int(spikes_file.addresses[i]))
                ts = struct.pack('>L', int(spikes_file.timestamps[i]//settings.ts_tick))
                f.write(addr)
                f.write(ts)
            if verbose == True:
                print("AEDAT file saved correctly.Took:", time.time() - start_time, 'seconds')


    @staticmethod
    def save_CSV(spikes_file, path, split = False, separator = ', ', verbose = False):
        """
        Saves a SpikesFile into a CSV file where each spike is represented in one line following the same patter: "address, timestamp".

        Parameters:
                spikes_file (SpikesFile): File to save.
                path (string): Path where the output file will be saved, including name. Extension should not be specified.
                split (boolean, optional): True for generating two files (addresses and timestamps), and False for generating one with all the information.
                separator (string, optional): which character to use as separator between addresses and timestamps when split = False
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        if verbose == True: start_time = time.time()
        if split == False:
            with open(path + '.csv', 'w') as f:
                for i in range(len(spikes_file.addresses)):
                    f.write(str(spikes_file.addresses[i]) + separator + str(int(spikes_file.timestamps[i])) + "\n")
        else:
            with open(path + '_addrs.csv', 'w') as f:
                for addr in spikes_file.addresses:
                    f.write(str(addr) + "\n")
            with open(path + '_tss.csv', 'w') as f:
                for ts in spikes_file.timestamps:
                    f.write(str(int(ts)) + '\n') 
        if verbose == True:
            print("CSV file saved correctly. Took:", time.time() - start_time, "seconds")


    @staticmethod
    def save_TXT(spikes_file, path, split = True, separator = ', ', verbose = False):
        """
        Saves a SpikesFile into two different TXT files, where addresses and timestamps are stored, respectively.

        Parameters:
                spikes_file (SpikesFile): File to save.
                path (string): Path where the output file will be saved, including name. Extension should not be specified.
                split (boolean, optional): True for generating two files (addresses and timestamps), and False for generating one with all the information.
                separator (string, optional): which character to use as separator between addresses and timestamps when split = False
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        if verbose == True: start_time = time.time()
        if split == True:
            with open(path + '_addrs.txt', 'w') as f:
                for addr in spikes_file.addresses:
                    f.write(str(addr) + '\n')
            with open(path + '_tss.txt', 'w') as f:
                for ts in spikes_file.timestamps:
                    f.write(str(int(ts)) + '\n')    
        else:
            with open(path + '.txt', 'w') as f:
                for i in range(len(spikes_file.addresses)):
                    f.write(str(spikes_file.addresses[i]) + separator + str(int(spikes_file.timestamps[i])) + '\n')
        if verbose == True:
            print("TXT file saved correctly. Took:", time.time() - start_time, "seconds")


    @staticmethod
    def save_TXT_relativeTS(spikes_file, path, split = True, separator = ', ', verbose = False):
        """
        Saves a SpikesFile into two different TXT files, where addresses and timestamps are stored, respectively. Timestamps are relative to the previous spike.

        Parameters:
                spikes_file (SpikesFile): File to save.
                path (string): Path where the output file will be saved, including name. Extension should not be specified.
                split (boolean, optional): True for generating two files (addresses and timestamps), and False for generating one with all the information.
                separator (string, optional): which character to use as separator between addresses and timestamps when split = False
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        spikes_file_ordered = Utils.order_timestamps(spikes_file)

        if verbose == True: start_time = time.time()

        if split == True:
            with open(path + '_addrs.txt', 'w') as f:
                for addr in spikes_file_ordered.addresses:
                    f.write(str(addr) + '\n')
            with open(path + '_tss.txt', 'w') as f:
                for i in range(len(spikes_file_ordered.timestamps)):
                    if i == 0:
                        f.write(str(0) + '\n')
                    else:
                        f.write(str(int(spikes_file_ordered.timestamps[i]-spikes_file_ordered.timestamps[i-1])) + '\n')
        else:
            with open(path + '_relativeTS.txt', 'w') as f:
                for i in range(len(spikes_file.addresses)):
                    if i == 0:
                        f.write(str(spikes_file.addresses[i]) + separator + str(0) + '\n')
                    else:
                        f.write(spikes_file.addresses[i] + separator + str(int(spikes_file_ordered.timestamps[i]-spikes_file_ordered.timestamps[i-1])) + '\n')
        if verbose == True:
            print("TXT file saved correctly. Took:", time.time() - start_time, "seconds")


    @staticmethod
    def save_as_any(spikes_file, path, output_format, settings=None):
        """
        Saves a SpikesFile into any of the implemented Savers, depending on the output format selected.

        Parameters:
                spikes_file (SpikesFile): File to save.                
                path (string): Path where the output file will be saved. Format should not be specified.
                output_format (string): Output format of the file. Currently supports '.aedat', '.csv', ".txt" and ".txt_rel". See the Savers class for more information.
                settings (MainSettings, optional): Configuration parameters for the output file. Only needed when saving the output as an AEDAT file.

        Returns:
                None.

        Raises:
                SettingsError: if settings are not specified and output_format refers to AEDAT.
        """

        if output_format in ['aedat', 'AEDAT', 'AEDAT', 'AEDAT', 'Aedat', '.aedat']:
            if settings != None:
                Savers.save_AEDAT(spikes_file, path, settings)
            else:
                print('[Savers.save_as_any] > SettingsError: Settings need to be specified when saving the file as an AEDAT filea.')                
        elif output_format in ['csv', 'CSV', '.csv']:
            Savers.save_CSV(spikes_file, path)
        elif output_format in ['txt', 'TXT', '.txt']:
            Savers.save_TXT(spikes_file, path)
        elif output_format in ['txt_rel', 'TXT_rel', '.txt_rel']:
            Savers.save_TXT_relativeTS(spikes_file, path)