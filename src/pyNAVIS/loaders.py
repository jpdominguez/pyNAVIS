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
import numpy as np


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

class LocalizationFile:
    """
    Class that contains all the events ant timestamps from the sound source localization model of a file.

    Attributes:
            mso_neurons_ids (int[]): Neuron's IDs of the MSO population of the file.
            mso_channels (int[]): Frequency channels associated to the MSO neuron's IDs of the file.
            mso_timestamps (int[]): Timestamps of the MSO neuron's IDs of the file.
            lso_neuron_ids (int[]): Neuron's IDs of the LSO population of the file.
            lso_channels (int[]): Frequency channels associated to the LSO neuron's IDs of the file.
            lso_timestamps (int[]): Timestamps of the LSO neuron's IDs of the file.
    
    Note:
            Timestamps, addresses, and neurons' ID are matched, which means that mso_timestamps[0] is the timestamp for the spike with address mso_neuron_ids[0].
    """

    def __init__(self, mso_neuron_ids = [], mso_channels = [], mso_timestamps = [], lso_neuron_ids = [], lso_channels = [], lso_timestamps = []):
        self.mso_neuron_ids = mso_neuron_ids
        self.mso_channels = mso_channels
        self.mso_timestamps = mso_timestamps
        self.lso_neuron_ids = lso_neuron_ids
        self.lso_channels = lso_channels
        self.lso_timestamps = lso_timestamps

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
        """
        # Read all the file
        file = open(path, "rb")
        file_data = file.read()

        # Find last header line
        end_string = "#End Of ASCII Header\r\n"
        index = file_data.find(end_string.encode("utf-8")) + len(end_string)

        # Raw data extraction
        num_spikes = int(math.floor(len(file_data[index:]) / (settings.address_size + settings.timestamp_size)))
        spikes_array = file_data[index:index + num_spikes * (settings.address_size + settings.timestamp_size)]

        address_param = ">u" + str(settings.address_size)
        timestamp_param = ">u" + str(settings.timestamp_size)
        bytes_struct = np.dtype(address_param + ", " + timestamp_param)

        spikes = np.frombuffer(spikes_array, bytes_struct)
        addresses = spikes['f0']
        timestamps = spikes['f1']

        spikes_file = SpikesFile(addresses, timestamps)

        # Close the file
        file.close()

        return spikes_file

    @staticmethod
    def loadAEDATLocalization(path, settings, localization_settings):
        """
        Loads an AEDAT (.aedat) file which contains events from both the NAS model and the SOC model (sound source localization).
        
        Parameters:
                path (string): Full path of the AEDAT file to be loaded, including name and extension.
                settings (MainSettings): Configuration parameters for the file to load.
                localization_settings (LocalizationSettings): Configuration parameters of the localization module for the file to load.
        Returns:
                SpikesFile: SpikesFile containing all the addresses and timestamps of the file.
                LocalizationFile: LocalizationFile containing all the events from both the MSO and LSO models of the file.
        Raises:
                SettingsError: If settings.address_size is different than 2 and 4.

        """
        unpack_param = ">H"

        if settings.address_size == 2:
            unpack_param = ">H"
        elif settings.address_size == 4:
            unpack_param = ">L"
        else:
            print("[Loaders.loadAEDATLocalization] > SettingsError: Only address sizes implemented are 2 and 4 bytes")

        # Check the localization_settings values
        localization_settings_error = False

        # MSO start frequency channel range
        if ((localization_settings.mso_start_channel < 0) or (localization_settings.mso_start_channel >= settings.num_channels)):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: MSO start frequency channel range should be in the range [0, num_channels-1]")
            localization_settings_error = True

        # MSO start frequency channel and end frequency channel
        if (localization_settings.mso_end_channel < localization_settings.mso_start_channel):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: MSO start frequency channel should be lower than MSO end frequency channel")
            localization_settings_error = True

        # MSO start frequency channel and end frequency channel
        if ((localization_settings.mso_num_neurons_channel < 1) or (localization_settings.mso_num_neurons_channel > 32)):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: MSO number of neurons value should be in the range [1, 32]")
            localization_settings_error = True

        # LSO start frequency channel range
        if ((localization_settings.lso_start_channel < 0) or (localization_settings.lso_start_channel >= settings.num_channels)):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: LSO start frequency channel range should be in the range [0, num_channels-1]")
            localization_settings_error = True

        # LSO start frequency channel and end frequency channel
        if (localization_settings.lso_end_channel < localization_settings.lso_start_channel):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: LSO start frequency channel should be lower than LSO end frequency channel")
            localization_settings_error = True

        # LSO start frequency channel and end frequency channel
        if ((localization_settings.lso_num_neurons_channel < 1) or (localization_settings.lso_num_neurons_channel > 32)):
            print("[Loaders.loadAEDATLocalization] > LocalizationSettingsError: lSO number of neurons value should be in the range [1, 32]")
            localization_settings_error = True

        if(localization_settings_error):
            return None

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

            events_nas = []
            timestamps_nas = []

            neuron_ids_mso = []
            channels_mso =  []
            timestamps_mso = []

            neuron_ids_lso = []
            channels_lso =  []
            timestamps_lso = []

            ## Read file ##
            i = 0
            total_number_events_counter = 0
            invalid_localization_data_counter = 0
            try:
                while 1:
                    # Read a word and unpack the event data
                    buff = f.read(settings.address_size)
                    ev = struct.unpack(unpack_param, buff)[0]
                    total_number_events_counter = total_number_events_counter + 1
                    # Read a word and unpack the event timestamp
                    buff = f.read(4)
                    ts = struct.unpack('>L', buff)[0]

                    # Check if the event is a NAS event of SOC event
                    auditory_model = (ev & 0x8000) >> 15

                    if auditory_model == 0:
                        # NAS event
                        events_nas.append(ev)
                        timestamps_nas.append(ts)
                    elif auditory_model == 1:
                        # Localization event

                        # Set the valid data flag to true
                        valid_localization_data = True

                        # Apply a mask to obtain the correct values and check them
                        neuron_id = (ev & 0x3E00) >> 9
                        if neuron_id < 0 or neuron_id >= localization_settings.mso_num_neurons_channel:
                            valid_localization_data = False
                        freq_channel = (ev & 0x00FE) >> 1
                        if freq_channel < localization_settings.mso_start_channel or freq_channel > localization_settings.mso_end_channel:
                            valid_localization_data = False

                        xso_type = (ev & 0x4000) >> 14

                        if xso_type == 0:
                            # MSO event
                            if valid_localization_data:
                                neuron_ids_mso.append(neuron_id)
                                channels_mso.append(freq_channel)
                                timestamps_mso.append(ts)
                            else:
                                invalid_localization_data_counter = invalid_localization_data_counter + 1
                        elif xso_type == 1:
                            # LSO event
                            neuron_ids_lso.append(neuron_id)
                            channels_lso.append(freq_channel)
                            timestamps_lso.append(ts)
                        else:
                            # Other case
                            print("[Loaders.loadAEDATLocalization] > DataError: MSO/LSO type not recognized!")
                    else:
                        # Other case
                        print("[Loaders.loadAEDATLocalization] > DataError: Auditory model not recognized!")

                    i += 1
            except Exception as inst:
                pass
        spikes_file = SpikesFile([], [])
        spikes_file.addresses = events_nas
        spikes_file.timestamps = timestamps_nas

        localization_file = LocalizationFile([], [], [], [], [], [])
        localization_file.mso_neuron_ids = neuron_ids_mso
        localization_file.mso_channels = channels_mso
        localization_file.mso_timestamps = timestamps_mso
        localization_file.lso_neuron_ids = neuron_ids_lso
        localization_file.lso_channels = channels_lso
        localization_file.lso_timestamps = timestamps_lso
        # Let the user know if there were dumped events
        if invalid_localization_data_counter > 0:
            print("[Loaders.loadAEDATLocalization] > DataWarning: " + str(invalid_localization_data_counter) + " of " + str(total_number_events_counter) + " were dumped due to invalid unpacked data!")
        return spikes_file, localization_file

    @staticmethod
    def loadCSV(path, delimiter=','):
        """
        Loads a Comma-Separated Values (.csv) file.
        
        Parameters:
                path (string): Full path of the CSV file to be loaded, including name and extension.
                delimiter (char): Delimiter to use in the CSV file.

        Returns:
                SpikesFile: SpikesFile containing all the addresses and timestamps of the file.

        Note:
                The CSV file should contain one line per event, and the information in each line should be: address, timestamp

        """
        addresses = []
        timestamps = []


        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            for row in csv_reader:
                addresses.append(int(row[0]))
                timestamps.append(int(row[1]))

        spikes_file = SpikesFile([], [])
        spikes_file.addresses = addresses
        spikes_file.timestamps = timestamps
        return spikes_file

    @staticmethod
    def loadCSVLocalization(path, delimiter=','):
        """
        Loads a Comma-Separated Values (.csv) file which contains events from both the NAS model and the SOC model (sound source localization).
        
        Parameters:
                path (string): Full path of the CSV file to be loaded, including name and extension.
                delimiter (char): Delimiter to use in the CSV file.

        Returns:
                SpikesFile: SpikesFile containing all the addresses and timestamps of the file.
                LocalizationFile: LocalizationFile containing all the events from both the MSO and LSO models of the file.

        Note:
                The CSV file should contain one line per event, and the information in each line should be: address, timestamp

                The CSV format should be: address, timestamp, auditory_model, xso_type, neuron_id.

        """
        addresses_nas = []
        timestamps_nas = []

        neuron_ids_mso = []
        channels_mso =  []
        timestamps_mso = []

        neuron_ids_lso = []
        channels_lso =  []
        timestamps_lso = []


        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            for row in csv_reader:

                try:
                    auditory_model = int(row[2])
                except Exception:
                    auditory_model = 0
                    pass

                address = int(row[0])
                timestamp = row[1]

                # Check if the timestamp contains any time reference (from simulation)
                timeref = "ps"
                if timeref in timestamp:
                    # Remove string "ps" and convert the timestamps from picoseconds to microseconds
                    timestamp = timestamp.replace(" ps", "")
                    timestamp = int(timestamp)
                    timestamp = timestamp * 1.0e-6

                if auditory_model == 0:
                    # NAS event
                    addresses_nas.append(address)
                    timestamps_nas.append(int(timestamp))
                elif auditory_model == 1:
                    # Localization event
                    xso_type = int(row[3])
                    neuron_id = int(row[4])

                    freq_channel = address #>> 1
                    if xso_type == 0:
                        # MSO event
                        neuron_ids_mso.append(neuron_id)
                        channels_mso.append(freq_channel)
                        timestamps_mso.append(timestamp)
                    elif xso_type == 1:
                        # LSO event
                        neuron_ids_lso.append(neuron_id)
                        channels_lso.append(freq_channel)
                        timestamps_lso.append(timestamp)
                    else:
                        # Other case
                        print("[Loaders.loadCSVLocalization] > DataError: MSO/LSO type not recognized!")
                else:
                    # Other case
                    print("[Loaders.loadCSVLocalization] > DataError: Auditory model not recognized!")

        spikes_file = SpikesFile([], [])
        spikes_file.addresses = addresses_nas
        spikes_file.timestamps = timestamps_nas

        localization_file = LocalizationFile([], [], [], [], [], [])
        localization_file.mso_neuron_ids = neuron_ids_mso
        localization_file.mso_channels = channels_mso
        localization_file.mso_timestamps = timestamps_mso
        localization_file.lso_neuron_ids = neuron_ids_lso
        localization_file.lso_channels = channels_lso
        localization_file.lso_timestamps = timestamps_lso

        return spikes_file, localization_file

    @staticmethod
    def loadZynqGrabberData(path, settings, localization_settings):
        """
        Loads a text (.txt) file with EAR events collected by the zynqGrabber.
        
        Parameters:
                path (string): Full path of the CSV file to be loaded, including name and extension.
                settings (MainSettings): Configuration parameters for the file to load.
                localization_settings (LocalizationSettings): Configuration parameters of the localization module for the file to load.

        Returns:
                spikes_file: SpikesFile containing all the addresses and timestamps of the file.
                localization_file: LocalizationFile containing all the events from both the MSO and LSO models of the file.
        """

        addresses = []
        timestamps = []

        neuron_ids_mso = []
        channels_mso =  []
        timestamps_mso = []

        neuron_ids_lso = []
        channels_lso =  []
        timestamps_lso = []

        txt_file = open(path, 'r')
        txt_lines = txt_file.readlines()

        count = 0
        for line in txt_lines:
            event = line.strip().split(',')
            decoded_events_timestamps      = float(event[0])
            decoded_events_auditory_models = int(event[1])           # 0 if the event comes from the NAS, 1 for the SOC model
            decoded_events_channels        = int(event[2])           # 0 left, 1 right
            decoded_events_xso_types       = int(event[3])           # 0 for MSO, 1 for LSO
            decoded_events_neuron_ids      = int(event[4])           # Between 0 and 15
            decoded_events_freq_ch_addrs   = int(event[5])           # Between 0 and 32
            decoded_events_polarities      = int(event[6])           # 0 pos, 1 neg

            # It could be either NAS (auditory_models = 0) or SOC events (auditory_models = 1)
            if decoded_events_auditory_models == 0:
                # NAS event
                timestamps.append(int(decoded_events_timestamps))
                addresses.append(int(decoded_events_freq_ch_addrs*(1+settings.on_off_both) + decoded_events_polarities +  settings.num_channels*decoded_events_channels*(1+settings.on_off_both)))

            elif decoded_events_auditory_models == 1:
                # It could be either MSO (xso_type = 0) or LSO events (xso_type = 1)
                if decoded_events_xso_types == 0:
                    # MSO event
                    timestamps_mso.append(int(decoded_events_timestamps))
                    channels_mso.append(int(decoded_events_freq_ch_addrs))
                    neuron_ids_mso.append(int(decoded_events_neuron_ids))

                elif decoded_events_xso_types == 1:
                    # LSO event
                    timestamps_lso.append(int(decoded_events_timestamps))
                    channels_lso.append(int(decoded_events_freq_ch_addrs))
                    neuron_ids_lso.append(int(decoded_events_neuron_ids))
                else:
                    # Other case
                    print("[Loaders.loadZynqGrabberData] > DataError: MSO/LSO type not recognized!")

            else:
                # Other case
                print("[Loaders.loadZynqGrabberData] > DataError: Auditory model not recognized!")

        spikes_file = SpikesFile([], [])
        spikes_file.addresses = addresses
        spikes_file.timestamps = timestamps

        localization_file = LocalizationFile([], [], [], [], [], [])
        localization_file.mso_neuron_ids = neuron_ids_mso
        localization_file.mso_channels = channels_mso
        localization_file.mso_timestamps = timestamps_mso
        localization_file.lso_neuron_ids = neuron_ids_lso
        localization_file.lso_channels = channels_lso
        localization_file.lso_timestamps = timestamps_lso

        return spikes_file, localization_file