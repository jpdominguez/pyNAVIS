import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, settings_localization):    
    stereo_file_nas, stereo_file_soc = Loaders.loadAEDATLocalization(path, settings, settings_localization)

    Functions.adapt_timestamps(stereo_file_nas, settings)
    Functions.check_SpikesFile(stereo_file_nas, settings)

    Functions.adapt_timestamps(stereo_file_soc, settings)
    Functions.check_LocalizationFile(stereo_file_soc, settings, settings_localization)
    
    Plots.spikegram(stereo_file_nas, settings)
    Plots.sonogram(stereo_file_nas, settings)
    Plots.histogram(stereo_file_nas, settings)
    Plots.average_activity(stereo_file_nas, settings)
    Plots.difference_between_LR(stereo_file_nas, settings)

    Plots.mso_spikegram(stereo_file_soc, settings, settings_localization)
    Plots.mso_heatmap(stereo_file_soc, settings_localization)
    Plots.mso_localization_plot(stereo_file_soc, settings, settings_localization)
    Plots.mso_histogram(stereo_file_soc, settings, settings_localization)

    plt.show()