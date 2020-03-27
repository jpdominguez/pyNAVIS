*********
Load file
*********


1. Load AER-DATA and CSV files
##############################

To load a file, the :doc:`Loaders <../pyNAVIS.loaders>` class needs to be used. Currently, only AER-DATA (.aedat) and Comma-Separated Values (.csv) files are supported.

For AER-DATA files, use the ``loadAERDATA()`` function by following this example:

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAERDATA('path/to/file/name.aedat', settings)

In this case, a file called ``name.aedat``, which is located in ``path/to/file/`` is loaded and stored into a :doc:`SpikesFile <../pyNAVIS.loaders>` variable named **spikes_info**.
For that, some configuration parameters need to be chosen for that specific file.
As it is shown in the code, this file consists of stereo (**mono_stereo=1**) information from 16 channels 
(**num_channels=16**), in which each channel has two addresses (for the positive and negative part of the 
signal; **on_off_both=1**). Also, in this AER-DATA file, addresses are stored using 2 bytes (**address_size=2**) 
and each timestamp value has to be multiplied by 0.2 (**ts_tick=0.2**) to match real time.

.. note::
    For the loadAERDAT function, the only parameter that is completely necessary is address_size.


On the other hand, to load a CSV file, follow the next example:

.. prompt:: python \

    from pyNAVIS import *
    spikes_info = Loaders.loadCSV('path/to/file/name.aedat')

Where no settings need to be specified.



2. Adapt and check SpikesFiles
##############################

Adapting a SpikesFile performs two different operations:

* First, the timestamps are multiplied by the **ts_tick** parameter of the MainSettings.
* Then, if **reset_timestamp** is set to True, the smallest timestamp in the file is subtracted to each of the other timestamps values.

Using the previous example, follow this lines of code to adapt the timestamps of a SpikesFile:

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAERDATA('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)

This function returns a new SpikesFile with the same information as the one used as input, but with the timestamps adapted.

Then, the ``check_SpikesFile()`` function can be used to check if the SpikesFile is correct. This function will:

* Check if all the timestamps of the SpikesFile are greater or equal than 0.
* Check if all the timestamps of the SpikesFile are ordered correctly.
* Check if all the addresses of the SpikesFile are between 0 and the maximum number of possible addresses, which depends on the settings.   

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAERDATA('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)
    Functions.check_SpikesFile(stereo_file, settings)

.. note::
    Both the adapt_SpikesFile() and the check_SpikesFile() functions are completely optional.


3. Plot information
##############################

To plot the spikegram (also known as cochleogram or raster plot), sonogram, histogram, average activity and the difference between left and right cochlea, follow the next example:

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAERDATA('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)
    Plots.spikegram(spikes_file_adapted, settings)
    Plots.sonogram(spikes_file_adapted, settings)
    Plots.histogram(spikes_file_adapted, settings)
    Plots.average_activity(spikes_file_adapted, settings)
    Plots.difference_between_LR(spikes_file_adapted, settings)


.. note::
    The difference between left and right cochlea can only be performed in stereo (mono_stereo=1) files.
