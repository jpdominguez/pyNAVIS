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

    def __init__(self, addresses=[], timestamps=[]):
        self.addresses = addresses
        self.timestamps = timestamps
        if len(timestamps) > 0:
            self.max_ts_index = np.argmax(timestamps)
            self.max_ts = timestamps[self.max_ts_index]
            self.min_ts_index = np.argmin(timestamps)
            self.min_ts = timestamps[self.min_ts_index]
        else:
            self.max_ts_index = None
            self.max_ts = None
            self.min_ts_index = None
            self.min_ts = None


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

    def __init__(self, mso_neuron_ids=[], mso_channels=[], mso_timestamps=[], lso_neuron_ids=[], lso_channels=[],
                 lso_timestamps=[]):
        self.mso_neuron_ids = mso_neuron_ids
        self.mso_channels = mso_channels
        self.mso_timestamps = mso_timestamps
        self.lso_neuron_ids = lso_neuron_ids
        self.lso_channels = lso_channels
        self.lso_timestamps = lso_timestamps