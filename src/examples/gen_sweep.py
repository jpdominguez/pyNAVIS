import matplotlib.pyplot as plt
from pyNAVIS import *
#############################################################################################################################

def run():
    sweep_spikes = Generators.sweep(freq=5, cycles=5, num_ch=64, length=1000000, return_save_both=0)
    sweep_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, bin_size=20000)
    Plots.spikegram(sweep_spikes, sweep_settings)
    Plots.sonogram(sweep_spikes, sweep_settings)
    Plots.histogram(sweep_spikes, sweep_settings)
    Plots.average_activity(sweep_spikes, sweep_settings)

    plt.show()