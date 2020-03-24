import matplotlib.pyplot as plt
from pyNAVIS import *

from examples import ex1

"""
#NOTE: Sweep
sweep_spikes = Generators.sweep(freq=5, cycles=5, num_ch=64, length=1000000, path='', return_save_both=0)
sweep_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, address_size=2, ts_tick=0.2, bin_size=1)
Plots.spikegram(sweep_spikes, sweep_settings)
#Plots.sonogram(sweep_spikes, sweep_settings)
#Plots.histogram(sweep_spikes, sweep_settings)
#Plots.average_activity(sweep_spikes, sweep_settings)
"""

ex1.run()

plt.show()