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
from bisect import bisect_left, bisect_right

from .functions import Functions
from .savers import Savers
from .utils import Utils

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
                outoutput_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.put_format.
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
            if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
                Savers.save_AERDATA(spikes_file_new, path + '.aedat', settings)
            elif output_format == 'csv' or 'CSV' or '.csv':
                Savers.save_CSV(spikes_file_new, path + '.csv', settings)        
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
            #save_AERDATA(splitted_aedat[i][0], splitted_aedat[i][1], str(i) +".aedat", settings)
        print cont
    """