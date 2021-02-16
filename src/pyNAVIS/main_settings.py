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
        num_channels (int): Number of cochlea channels.
        address_size (int): Number of bytes that each address is using. Only needed when loading .aedat files
        on_off_both (int): Select wether the addresses contained in the file are ON, OFF or if it is using both.
        reset_timestamp (boolean): Select wether to have timedtamps starting at 0 (True) or leave it as they are (False).
    
    Notes:
            Set ts_tick to 1 for .aedat files recorded with jAER, to 0.2 for files recorded with USBAERmini2, and to 80e-3 for files recorded with zynqGrabber.

            Set address_size to 2 for .eadat files recorded with USBAERmini2, or to 4 for files recorded with jAER.
            This parameter is only relevant for loading AEDAT (.aedat) files.

            Set on_off_both to 0 if addresses are only ON or OFF, or to 1 if using both ON and OFF.

            reset_timestamp subtracts the smallest timestamp in the file to each of the timestamps.
    """

    def __init__(self, num_channels, mono_stereo = 0, address_size = 2, ts_tick = 1, bin_size = 20000, on_off_both = 1, reset_timestamp = True):
        self.num_channels = num_channels
        self.mono_stereo = mono_stereo
        self.address_size = address_size
        self.ts_tick = ts_tick
        self.bin_size = bin_size
        self.on_off_both = on_off_both
        self.reset_timestamp = reset_timestamp

class LocalizationSettings:
    """
    Class that collects the configuration settings of pyNAVS when working with a NAS model that integrates the sound source localization model

    Attributes:
        mso_start_channel (int): First NAS frequency channel that is connected to the MSO module.
        mso_end_channel (int): Last NAS frequency channel that is connected to the MSO module.
        mso_num_neurons_channel (int): Number of coincidence detector neurons used for each frequency channel in the MSO module.
        lso_start_channel (int): First NAS frequency channel that is connected to the LSO module.
        lso_end_channel (int): Last NAS frequency channel that is connected to the LSO module.
        lso_num_neurons_channel (int): Number of neurons used for each frequency channel in the LSO module.

    Notes:
            The first frequency channel is the channel number 0.

            The frequency channel range should coincide with the parameter num_channels set in MainSettings.

            The values set here should be the same that the one used for generating the FPGA configuration file.
    """

    def __init__(self, mso_start_channel, mso_end_channel, mso_num_neurons_channel, lso_start_channel = 0, lso_end_channel = 1, lso_num_neurons_channel = 1):
        self.mso_start_channel = mso_start_channel
        self.mso_end_channel = mso_end_channel
        self.mso_num_neurons_channel = mso_num_neurons_channel
        self.lso_start_channel = lso_start_channel
        self.lso_end_channel = lso_end_channel
        self.lso_num_neurons_channel = lso_num_neurons_channel