******************************************************
Generate image datasets from spiking information
******************************************************


With this functionality you can generate a set of sonogram images from a folder where files are.

.. prompt:: python \

    from pyNAVIS import *

    input_folder            = 'path/to/input_folder'    # folder that contains the files with spikes
    output_folder           = 'path/to/output_folder'   # folder where the sonograms will be saved
    allow_subdirectories    = False                     # look into subdirectories within input_folder

    settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=20000)

    DatasetGenerators.generate_sonogram_dataset(input_folder, output_folder, settings, allow_subdirectories=allow_subdirectories)

.. note::
    Currently, this functionality only supports AEDAT (.aedat) files.