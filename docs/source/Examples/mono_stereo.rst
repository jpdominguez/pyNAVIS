**************************************************
Convert from mono to stereo files and vice versa
**************************************************

From mono to stereo
###################

To convert from a mono SpikesFile to a stereo SpikesFile, first load the mono file:

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    mono_file = Loaders.loadAEDAT('path/to/file/name.aedat', settings)

.. warning::
    Pay attention to the **mono_stereo** parameter, which was set to 0, meaning that the file that is loaded is mono.

Then execute the ``mono_to_stereo()`` function:

.. prompt:: python \

    stereo_file = Functions.mono_to_stereo(mono_file, delay=0, settings=settings, return_save_both=0)
    
Where **delay** is the time delay between left and right information.

.. note::
    
    When **return_save_both** is set to 0, the information will be returned as a SpikesFile. If it is set to 1, the information will be saved instead of being returned. If it is set to 2, the information will be returned and also saved.

    If **return_save_both** is set to either 1 or 2, you also have to set the **path** where the file will be saved, and the **output_format**. Check the :doc:`mono_to_stereo() <../pyNAVIS.functions>` function for more information.


To plot the output file, you can use the graphs presented in :doc:`previous examples <Load file>`.

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    mono_file = Loaders.loadAEDAT('path/to/file/name.aedat', settings)
    stereo_file = Functions.mono_to_stereo(mono_file, delay=0, settings=settings, return_save_both=0)
    settings.mono_stereo = 1
    Plots.spikegram(stereo_file, settings)

.. warning::
    To plot the information, **mono_stereo** has to be set to 1.



From stereo to mono
###################

The same procedure, but using the ``stereo_to_mono()``, can be applied to convert a stereo file to a mono file:

.. prompt:: python \

    from pyNAVIS import *
    settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
    stereo_file = Loaders.loadAEDAT('path/to/file/name.aedat', settings)
    mono_file = Functions.stereo_to_mono(stereo_file, left_right=0, settings=settings, return_save_both=0)
    settings.mono_stereo = 0
    Plots.spikegram(mono_file, settings)

For more information regarding this function, see :doc:`stereo_to_mono() <../pyNAVIS.functions>`.