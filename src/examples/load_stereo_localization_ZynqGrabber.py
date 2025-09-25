import matplotlib.pyplot as plt
from pyNAVIS import *


def run(path, settings, settings_localization):    
    stereo_file_nas, stereo_file_soc = Loaders.loadZynqGrabberData(path, settings, settings_localization)

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

    Functions.PDF_report(stereo_file_nas, settings, path.replace('.txt', '.pdf'), plots=["Sonogram", "Histogram", "Average activity"], add_localization_report = True, localization_file = stereo_file_soc, localization_settings = settings_localization, localization_plots = ["MSO spikegram", "MSO heatmap", "MSO histogram", "MSO localization"], vector=False)