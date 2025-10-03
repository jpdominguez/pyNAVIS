import matplotlib.pyplot as plt
from pyNAVIS import *
#############################################################################################################################

def run():
    sweep_spikes = Generators.sweep(freq=20, cycles=5, num_ch=256, length=1000000, return_save_both=2, path='sweep_20Hz_5cyc_256ch.aedat')
    sweep_settings = MainSettings(num_channels=128, mono_stereo=1, on_off_both=0, bin_size=20000)
    Plots.spikegram(sweep_spikes, sweep_settings)
    Plots.sonogram(sweep_spikes, sweep_settings)
    Plots.histogram(sweep_spikes, sweep_settings)
    Plots.average_activity(sweep_spikes, sweep_settings)

    plt.show()