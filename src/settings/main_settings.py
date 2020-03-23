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

class MainSettings:
    """
    Class that collects the main configuration settings of pyNAVIS

    Attributes:
        mono_stereo (int): Set to 0 for mono files and 1 for stereo files.
        bin_size (int): Bin width (or window size) to use when processing the information.
        ts_tick (float): Timestamp tick. Correspondence factor between timestamp value in file and actual time.
            NOTE: Set it to 1 for .aedat files recorded with jAER, or to 0.2 for files recorded with USBAERmini2.
        num_channels (int): Number of cochlea channels.
        address_size (int): Number of bytes that each address is using.
            NOTE: Set it to 2 for .eadat files recorded with USBAERmini2, or to 4 for files recorded with jAER.
            NOTE: This parameter is only relevant for loading AER-DATA 8.aedat) files.
        on_off_both (int): Select wether the addresses contained in the file are ON, OFF or if it is using both.
            NOTE: Set it to 0 if addresses are only ON, to 1 if addresses are only OFF, or to 2 if using both ON and OFF.
        reset_timestamp (boolean): Select wether to have timedtamps starting at 0 (True) or leave it as they are (False).
            NOTE: This subtracts  the smallest timestamp in the file to each of the timestamps.
        spikegram_dot_size (float): Size of the dots used in the spikegram plot.
        bar_line (int): Select wether to plot the histogram and the average activity plots as bar plots or as line graphs.
        spikegram_dot_freq (int): Set the frequency of spikes that will be represented in the spikegram.
            NOTE: A value of 10 means that for every 10 spikes, only 1 will be plotted.
            NOTE: This helps reducing lag when plotting heavy files.
    """

    mono_stereo = 0
    bin_size = 20000
    ts_tick = 0.2
    num_channels = 32
    address_size = 2
    on_off_both = 2
    reset_timestamp = True
    spikegram_dot_size = 0.2
    bar_line = 1
    spikegram_dot_freq = 1

    def __init__(self, num_channels, mono_stereo, address_size = 2, ts_tick = 0.2, bin_size = 20000, on_off_both = 2, reset_timestamp = True, spikegram_dot_size = 0.2, bar_line = 1, spikegram_dot_freq = 1):
        self.num_channels = num_channels
        self.mono_stereo = mono_stereo
        self.address_size = address_size
        self.ts_tick = ts_tick
        self.bin_size = bin_size
        self.on_off_both = on_off_both
        self.reset_timestamp = reset_timestamp
        self.spikegram_dot_size = spikegram_dot_size
        self.bar_line = bar_line
        self.spikegram_dot_freq = spikegram_dot_freq