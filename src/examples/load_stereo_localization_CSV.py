import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, settings_localization, include_nas = True):    
    stereo_file_nas, stereo_file_soc = Loaders.loadCSVLocalization(path, delimiter=',')

    if include_nas == True:
        Functions.adapt_timestamps(stereo_file_nas, settings)
        Functions.check_SpikesFile(stereo_file_nas, settings)

    Functions.adapt_timestamps(stereo_file_soc, settings)
    Functions.check_LocalizationFile(stereo_file_soc, settings, settings_localization)
    
    if include_nas == True:
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