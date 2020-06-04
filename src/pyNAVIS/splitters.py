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


import copy
import random
import numpy as np
import time
from bisect import bisect_left, bisect_right

from .functions import Functions
from .savers import Savers
from .utils import Utils
from .loaders import SpikesFile

class Splitters:

    @staticmethod
    def manual_splitter(spikes_file, init, end, settings,  return_save_both = 0, output_format = '.aedat', path=None):
        """
        Extract a portion of the input SpikesFile file.

        Parameters:
                spikes_file (SpikesFile): Input file.
                init (int): First timestamp from which to start extracting. 
                end (int): Last timestamp from which to stop extracting. 
                settings (MainSettings): Configuration parameters for the input file.
                return_save_both (int, optional): Set it to 0 to return the resultant SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
                output_format (string, optional): Output format of the file. Currently supports '.aedat', '.csv', ".txt" and ".txt_rel". See the Savers class for more information.
                path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.

        Returns:
                SpikesFile: SpikesFile containing the extracted portion of the input file. Returned only if return_save_both is either 0 or 2.
        """

        #THIS IS NOT NEEDED IF TS ARE SORTED
        aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
        aedat_addr_ts = sorted(aedat_addr_ts, key=Utils.getKey)
        spikes_file_new = copy.deepcopy(spikes_file)
        spikes_file_new = Utils.extract_addr_and_ts(aedat_addr_ts)

        a =  bisect_left(spikes_file_new.timestamps, init)
        b =  bisect_right(spikes_file_new.timestamps, end)

        spikes_file_new.addresses = spikes_file_new.addresses[a:b]
        spikes_file_new.timestamps = spikes_file_new.timestamps[a:b]

        if return_save_both == 0:
            return spikes_file_new
        elif return_save_both == 1 or return_save_both == 2:
            Savers.save_as_any(spikes_file_new, path=path, output_format=output_format, settings=settings) 
            if return_save_both == 2:
                return spikes_file_new

    """
    def automatic_aedat_splitter(allAddr, allTs, noiseTolerance, noiseThreshold, settings, path):
        #THIS IS NOT NEEDED IF TS ARE SORTED
        aedat_addr_ts = zip(allAddr, allTs)
        aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
        allAddr, allTs = extract_addr_and_ts(aedat_addr_ts)

        total_time = max(allTs) - min(allTs)
        last_time = min(allTs)
        its = int(math.ceil(total_time/settings.bin_size))
        numb_spikes_file = len(allAddr)

        hasEntered = 0
        times_entered = 0
        current_split = []
        splitted_aedat = []
        split_index = 0


        for i in range(its):

            a =  bisect_left(allTs, last_time)
            b =  bisect_right(allTs, last_time + settings.bin_size)
            blockAddr = allAddr[a:b]
            blockTs = allTs[a:b]

            #print len(blockAddr)
            #print noiseThreshold * numb_spikes_file
            if len(blockAddr) < noiseThreshold * numb_spikes_file:
                if hasEntered:
                    hasEntered = 0
                    current_split = []
                    split_index += 1

                    if times_entered < noiseTolerance:
                        splitted_aedat[split_index-1] = []
                    times_entered = 0
            else:
                current_split.append([blockAddr, blockTs])
                splitted_aedat.append(current_split)
                hasEntered = 1
                times_entered += 1

            last_time += settings.bin_size

        cont  = 0
        for i in range(len(splitted_aedat)):
            if len(splitted_aedat[i]) > 1:
                cont += 1
                print len(splitted_aedat[i])
            #save_AEDAT(splitted_aedat[i][0], splitted_aedat[i][1], str(i) +".aedat", settings)
        print cont
    """



    @staticmethod
    def segmenter_RT(spikes_file, noise_threshold, bin_width, return_save_both = 0, output_format = '.aedat', path=None, settings = None, verbose = False):
        """
        Removes background noise.

        A FIFO of size noise_threshold will be filling up with every spike. If the timestamp difference between the \
             first and the last spike in the FIFO is lower or equal than bin_width, then the most recent spike is saved.

        Parameters:
                spikes_file (SpikesFile): Input file.
                noise_threshold (int): Size of the FIFO. 
                bin_width (int): Time difference (in ms).
                return_save_both (int, optional): Set it to 0 to return the resultant SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
                output_format (string, optional): Output format of the file. Currently supports '.aedat', '.csv', ".txt" and ".txt_rel". See the Savers class for more information.
                path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                settings (MainSettings, optional): Configuration parameters for the output file. Only needed when saving the output as an AEDAT file.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                SpikesFile: SpikesFile containing the processed input file. Returned only if return_save_both is either 0 or 2.
        """

        current_ts = 0  # Timestamp of the current spike that it's being processed.
        spikes_processed = 0    # Number of spikes processed. Used to avoid saving spikes before the FIFO has filled completely.
        buffer_ts = np.zeros(int(noise_threshold))  # FIFO.
        spikes_filtered = SpikesFile([], [])  # SpikesFile where the output will be saved.

        if verbose == True: start_time = time.time()

        for i in range(len(spikes_file.timestamps)):
            current_ts = spikes_file.timestamps[i]
            current_addr = spikes_file.addresses[i]

            buffer_ts = np.roll(buffer_ts, -1)  # Shifting the information of the FIFO.
            buffer_ts[-1] = current_ts

            spikes_processed +=1

            if ((current_ts - buffer_ts[0]) <= bin_width * 1000) and (spikes_processed >= noise_threshold):
                spikes_filtered.addresses.append(current_addr)
                spikes_filtered.timestamps.append(current_ts) 

        if verbose == True: print('SEGMENTER_RT CALCULATION', time.time() - start_time)

        if return_save_both == 0:
            return spikes_filtered
        elif return_save_both == 1 or return_save_both == 2:
            Savers.save_as_any(spikes_filtered, path=path, output_format=output_format) 
            if return_save_both == 2:
                return spikes_filtered