import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, delay = 0):

    spikes_file = Loaders.loadAEDAT(path, settings)
    spikes_file = Functions.adapt_SpikesFile(spikes_file, settings)
    Functions.check_SpikesFile(spikes_file, settings)
    Plots.spikegram(spikes_file, settings, verbose=True)
    
    phaselocked_file = Functions.phase_lock(spikes_file, settings)
    settings.on_off_both = 0
    Plots.spikegram(phaselocked_file, settings)
    
    plt.show()