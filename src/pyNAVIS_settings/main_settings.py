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