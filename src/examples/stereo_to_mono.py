import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, left_right = 0):

    spikes_file = Loaders.loadAEDAT(path, settings)
    spikes_file = Functions.adapt_SpikesFile(spikes_file, settings)
    Functions.check_SpikesFile(spikes_file, settings)
    Plots.spikegram(spikes_file, settings, verbose=True)

    mono_file = Functions.stereo_to_mono(spikes_file, left_right = left_right, return_save_both = 0, settings = settings)    
    settings.mono_stereo = 0
    Plots.spikegram(mono_file, settings)

    plt.show()