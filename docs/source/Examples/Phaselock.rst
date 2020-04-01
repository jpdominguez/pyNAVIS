******************************************************
Phaselock
******************************************************



An interesting functionality that is supported in this software package is the phaselock operation.

The phaselock operation puts a spike in the output only when the spike train from a specific channel changes from ON (positive part of the signal) to OFF (negative part of the signal). This heavily reduces the number of spikes at the output.

.. note::
    This functionality can only be used in files that have two addresses per channel (ON and OFF). The settings should also match this (on_off_both has to be equal to 1).


See the following example:

.. prompt:: python \

    from pyNAVIS import *

    settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    spikes_info = Loaders.loadAERDATA('path/to/file/name.aedat', settings)
    spikes_file_adapted = Functions.adapt_SpikesFile(spikes_info, settings)

    phaselocked_file = Functions.phase_lock(spikes_file_adapted, settings)

.. warning::
    If you want to plot the output, the settings should be changed before plotting, since the phaselock operation fuses ON and OFF addresses into only one (on_off_both should be set to 0).