import matplotlib.pyplot as plt
from pyNAVIS import *
#############################################################################################################################

## PARAMETERS ###############################################################################################################
num_channels = 32      # Number of NAS channels (not addresses but channels).                                               #
mono_stereo = 0        # 0 for a monaural NAS or 1 for a binaural NAS.                                                      #
address_size = 2       # 2 if .aedats are recorded with USBAERmini2 or 4 if .aedats are recorded with jAER.                 #
ts_tick = 0.2          # 0.2 if .aedats are recorded with USBAERmini2 or 1 if .aedats are recorded with jAER.               #
bin_size = 20000       # Time bin (in microseconds) used to integrate the spiking information.                              #
#############################################################################################################################


def run():
    sweep_spikes = Generators.random_addrs(freq=1000, num_ch=64, length=1000000, path='', return_save_both=0)
    sweep_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size)
    Plots.spikegram(sweep_spikes, sweep_settings)
    Plots.sonogram(sweep_spikes, sweep_settings)
    Plots.histogram(sweep_spikes, sweep_settings)
    Plots.average_activity(sweep_spikes, sweep_settings)

    plt.show()