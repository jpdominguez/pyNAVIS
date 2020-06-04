import matplotlib.pyplot as plt
from pyNAVIS import *



def run(path, settings):

    # Load file
    spikes_file = Loaders.loadAEDAT(path, settings)
    spikes_file = Functions.adapt_SpikesFile(spikes_file, settings)
    Functions.check_SpikesFile(spikes_file, settings)
    Plots.spikegram(spikes_file, settings, verbose=True)
    Plots.sonogram(spikes_file, settings, verbose=True)
    Plots.histogram(spikes_file, settings, verbose=True)
    Plots.average_activity(spikes_file, settings, verbose=True)
    Plots.difference_between_LR(spikes_file, settings, verbose=True)
    


    manual_split_spikes = Splitters.manual_splitter(spikes_file, init=0, end=100000, settings=settings, return_save_both=0)
    Plots.spikegram(manual_split_spikes, settings, graph_tile='Splitted SpikesFile spikegram', verbose=True)
    Plots.sonogram(manual_split_spikes, settings, graph_tile='Splitted SpikesFile sonogram', verbose=True)

    plt.show()
