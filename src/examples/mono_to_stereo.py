import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, delay = 0):

    spikes_file = Loaders.loadAEDAT(path, settings)
    spikes_file = Functions.adapt_SpikesFile(spikes_file, settings)
    Functions.check_SpikesFile(spikes_file, settings)
    Plots.spikegram(spikes_file, settings, verbose=True)
    
    stereo_file = Functions.mono_to_stereo(spikes_file, delay=delay, settings=settings, return_save_both=0)
    settings.mono_stereo = 1
    Plots.spikegram(stereo_file, settings)
    
    plt.show()