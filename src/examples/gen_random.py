import matplotlib.pyplot as plt
from pyNAVIS import *
#############################################################################################################################

def run():
    rand_spikes = Generators.random_addrs(freq=1000, num_ch=64, length=1000000, return_save_both=2, path='C:\\Users\\juado\\Downloads\\Telegram Desktop\\Random_addrs.aedat')
    rand_settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=0, bin_size=20000)
    Plots.spikegram(rand_spikes, rand_settings)
    Plots.sonogram(rand_spikes, rand_settings)
    Plots.histogram(rand_spikes, rand_settings)
    Plots.average_activity(rand_spikes, rand_settings)

    plt.show()