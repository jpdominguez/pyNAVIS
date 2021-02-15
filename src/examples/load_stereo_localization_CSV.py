import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, settings_localization, include_nas = True):    
    stereo_file_nas, stereo_file_soc = Loaders.loadCSVLocalization(path, delimiter=',', from_simulation=True)

    if include_nas == True:
        stereo_file_nas.timestamps = Functions.adapt_timestamps(stereo_file_nas.timestamps, settings)
        Functions.check_SpikesFile(stereo_file_nas, settings)

    stereo_file_soc.mso_timestamps = Functions.adapt_timestamps(stereo_file_soc.mso_timestamps, settings)
    Functions.check_LocalizationFile(stereo_file_soc, settings, settings_localization)
    
    if include_nas == True:
        Plots.spikegram(stereo_file_nas, settings)
        Plots.sonogram(stereo_file_nas, settings)
        Plots.histogram(stereo_file_nas, settings)
        Plots.average_activity(stereo_file_nas, settings)
        Plots.difference_between_LR(stereo_file_nas, settings)

    Plots.mso_spikegram(stereo_file_soc, settings, settings_localization)
    Plots.mso_heatmap(stereo_file_soc, settings_localization)
    Plots.mso_localization(stereo_file_soc, settings, settings_localization)
    Plots.mso_histogram(stereo_file_soc, settings, settings_localization)

    plt.show()