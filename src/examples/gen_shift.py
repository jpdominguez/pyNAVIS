import matplotlib.pyplot as plt
from pyNAVIS import *
#############################################################################################################################

def run():
    shift_spikes = Generators.shift(freq=10, num_ch=64, length=1000000, return_save_both=0)
    shift_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, bin_size=20000)
    Plots.spikegram(shift_spikes, shift_settings)
    Plots.sonogram(shift_spikes, shift_settings)
    Plots.histogram(shift_spikes, shift_settings)
    Plots.average_activity(shift_spikes, shift_settings)

    plt.show()