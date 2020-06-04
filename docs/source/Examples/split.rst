******************************************************
Manually split spiking information
******************************************************

With ``pyNAVIS`` you can both select a specific portion of time from a file and extract it, and also get the information from a set of addresses which can be specified by the user.

1. Extract a portion of the file
################################

To do this, you should use the ``manual_splitter()`` function from the :doc:`Splitters class <../pyNAVIS.splitters>`.

Here you can find an example where a file is loaded and then a portion of it is extracted (from 0 to 100000 microseconds):

.. prompt:: python \

    from pyNAVIS import *

    init_timestamp = 0          # microseconds
    end_timestamp  = 100000     # microseconds

    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAEDAT('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)

    manual_split_spikes = Splitters.manual_splitter(spikes_file_adapted, init=init_timestamp, end=end_timestamp, settings=settings, return_save_both=0)


Whose information can be saved into a file, plotted, or processed.



2. Extract a set of addresses from the file
###########################################

You can also extract a user-defined set of addresses from a file.

To do this, you should use the ``extract_channels_activities()`` function from the :doc:`Functions class <../pyNAVIS.functions>`.

See the following example:

.. prompt:: python \

    from pyNAVIS import *

    addresses_set = [0, 1, 2, 3]   # List of addresses to extract from the file. Can also be set with range(4).

    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAEDAT('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)

    addresses_info = Functions.extract_channels_activities(spikes_file_adapted, addresses=addresses_set)

If you want to plot **addresses_info**, the settings should be changed to support the number of addresses that this new variable has.

