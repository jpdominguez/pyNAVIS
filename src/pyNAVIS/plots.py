#################################################################################
##                                                                             ##
##    Copyright C 2018  Juan P. Dominguez-Morales                              ##
##                                                                             ##
##    This file is part of pyNAVIS.                                            ##
##                                                                             ##
##    pyNAVIS is free software: you can redistribute it and/or modify          ##
##    it under the terms of the GNU General Public License as published by     ##
##    the Free Software Foundation, either version 3 of the License, or        ##
##    (at your option) any later version.                                      ##
##                                                                             ##
##    pyNAVIS is distributed in the hope that it will be useful,               ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the              ##
##    GNU General Public License for more details.                             ##
##                                                                             ##
##    You should have received a copy of the GNU General Public License        ##
##    along with pyNAVIS.  If not, see <http://www.gnu.org/licenses/>.         ##
##                                                                             ##
#################################################################################

import math
import random
import time
from bisect import bisect_left, bisect_right

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


class Plots:
    @staticmethod
    def spikegram(spikes_file, settings, dot_size=0.2, dot_freq=1, graph_title='Spikegram', start_at_zero=True,
                  verbose=False):
        """
        Plots the spikegram (also known as cochleogram or raster plot) of a SpikesFile.

        This is, a graph where the X axis means time and the Y axis represents addresses (or cochlea channels), and where every spike is plotted as a dot.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                dot_size (float): Size of the dots used in the spikegram plot.
                dot_freq (int): Set the frequency of spikes that will be represented in the spikegram.
                graph_title (string, optional): Text that will appear as title for the graph.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note:
                A value of 10 in dot_freq means that for every 10 spikes, only 1 will be plotted. This helps reducing lag when plotting heavy files.
        """
        if verbose:
            start_time = time.time()
        # REPRESENTATION
        plt.style.use('seaborn-whitegrid')
        spk_fig = plt.figure()
        spk_fig.canvas.set_window_title(graph_title)

        random.seed(0)

        mid_address = settings.num_channels * (settings.on_off_both + 1)

        if settings.mono_stereo == 0:
            plt.scatter(spikes_file.timestamps[0::dot_freq], spikes_file.addresses[0::dot_freq],
                        s=dot_size, rasterized=True)
        else:
            # Convert to numpy arrays
            addresses = np.array(spikes_file.addresses, copy=False)
            timestamps = np.array(spikes_file.timestamps, copy=False)

            sup_indexes = np.argwhere(addresses >= mid_address)

            sup_addresses = addresses[sup_indexes]
            sup_addresses = sup_addresses[::dot_freq]
            sup_timestamps = timestamps[sup_indexes]
            sup_timestamps = sup_timestamps[::dot_freq]

            inf_addresses = addresses[-sup_indexes]
            inf_addresses = inf_addresses[::dot_freq]
            inf_timestamps = timestamps[-sup_indexes]
            inf_timestamps = inf_timestamps[::dot_freq]

            plt.scatter(inf_timestamps, inf_addresses, s=dot_size, label="Left cochlea", rasterized=True)
            plt.scatter(sup_timestamps, sup_addresses, s=dot_size, label="Right cochlea", rasterized=True)
            plt.legend(fancybox=False, ncol=2, loc='upper center', markerscale=2 / dot_size, frameon=True)

        if verbose:
            print('SPIKEGRAM CALCULATION', time.time() - start_time)

        plt.title(graph_title, fontsize='x-large')
        plt.xlabel('Timestamp ($\mu$s)', fontsize='large')
        plt.ylabel('Address', fontsize='large')
        plt.ylim([0, mid_address * (settings.mono_stereo + 1)])

        if start_at_zero:
            max_timestamp = np.max(spikes_file.timestamps)
            plt.xlim([0, max_timestamp])

        plt.tight_layout()

        return spk_fig

    @staticmethod
    def sonogram(spikes_file, settings, return_data=False, graph_title='Sonogram', start_at_zero=True, verbose=False):
        """
        Plots the sonogram of a SpikesFile.

        This is, a graph where the X axis means time and the Y axis represents addresses (or cochlea channels), and where the spiking activity is shown with color.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                return_data (boolean, optional): When set to True, the sonogram matrix will be returned instead of plotted.
                graph_title (string, optional): Text that will appear as title for the graph.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[ , ]: Sonogram matrix. Only returned if return_data is set to True.
        """
        if verbose:
            start_time = time.time()

        # Convert to numpy array
        timestamps = np.array(spikes_file.timestamps, copy=False)

        # Check start
        if start_at_zero:
            total_time = np.max(timestamps)
            last_time = 0
        else:
            min_timestamp = np.min(timestamps)
            total_time = np.max(timestamps) - min_timestamp
            last_time = min_timestamp

        # Calculate number of addresses and number of windows
        num_addresses = settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)
        num_windows = int(math.ceil(total_time / settings.bin_size))

        # Define sonogram array
        sonogram = np.zeros((num_addresses, num_windows))

        # Bincount
        for i in range(num_windows):
            a = bisect_left(spikes_file.timestamps, last_time)
            b = bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

            blockAddr = spikes_file.addresses[a:b]

            spikes = np.bincount(blockAddr, minlength=num_addresses)

            last_time += settings.bin_size
            sonogram[:, i] = spikes

        if verbose:
            print('SONOGRAM CALCULATION', time.time() - start_time)

        if not return_data:
            # REPRESENTATION
            plt.style.use('default')
            sng_fig = plt.figure()
            sng_fig.canvas.set_window_title(graph_title)

            plt.imshow(sonogram, aspect="auto", cmap='hot', rasterized=True)  # , aspect="auto")
            plt.gca().invert_yaxis()

            plt.xlabel('Bin (' + str(settings.bin_size) + '$\mu$s width)', fontsize='large')
            plt.ylabel('Address', fontsize='large')

            plt.title(graph_title, fontsize='x-large')

            """
            plt.annotate('Right cochlea | Left cochlea',
            xy=(1.00, 0.5), xytext=(5, 0),
            xycoords=('axes fraction', 'figure fraction'),
            textcoords='offset points',
            size=11, ha='center', va='center', rotation=270)
            """

            if settings.mono_stereo == 1:
                plt.annotate('Right cochlea',
                             xy=(1.00, 0.75), xytext=(5, 0),
                             xycoords=('axes fraction', 'axes fraction'),
                             textcoords='offset points',
                             size=11, ha='center', va='center', rotation=270)

                plt.annotate('Left cochlea',
                             xy=(1.00, 0.25), xytext=(5, 0),
                             xycoords=('axes fraction', 'axes fraction'),
                             textcoords='offset points',
                             size=11, ha='center', va='center', rotation=270)

            colorbar = plt.colorbar()
            colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad=10)

            return sng_fig
        else:
            return sonogram

    @staticmethod
    def histogram(spikes_file, settings, bar_line=1, graph_title='Histogram', verbose=False):
        """
        Plots the histogram of a SpikesFile.

        This is, a graph where addresses (or cochlea channels) are represented in the X axis, and number of spikes in the Y axis.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                bar_line (int, optional): Select wether to plot the histogram as bar plot (0) or as a line graph (1).
                graph_title (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[]: Histogram array.
        """

        start_time = time.time()

        spikes_count = np.bincount(spikes_file.addresses,
                                   minlength=settings.num_channels * (settings.on_off_both + 1) * (
                                               settings.mono_stereo + 1))

        if verbose == True: print('HISTOGRAM CALCULATION:', time.time() - start_time)

        plt.style.use('seaborn-whitegrid')
        hst_fig = plt.figure()
        hst_fig.canvas.set_window_title(graph_title)
        plt.title(graph_title, fontsize='x-large')
        plt.xlabel('Address', fontsize='large')
        plt.ylabel('No. of spikes', fontsize='large')

        if bar_line == 0:
            if settings.mono_stereo == 1:
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1)),
                        spikes_count[0:settings.num_channels * (settings.on_off_both + 1)],
                        rasterized=True)
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1)),
                        spikes_count[settings.num_channels * (settings.on_off_both + 1):settings.num_channels * 2 * (settings.on_off_both + 1)],
                        rasterized=True)
            else:
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)),
                        spikes_count, rasterized=True)
        else:
            if settings.mono_stereo == 1:
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1)),
                         spikes_count[0:settings.num_channels * (settings.on_off_both + 1)],
                         label='Left cochlea', rasterized=True)
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1)),
                         spikes_count[settings.num_channels * (settings.on_off_both + 1):settings.num_channels * 2 * (settings.on_off_both + 1)],
                         label='Right cochlea', rasterized=True)
                plt.legend(loc='best', frameon=True)
            else:
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)),
                         spikes_count, rasterized=True)

        plt.tight_layout()

        return spikes_count, hst_fig

    @staticmethod
    def average_activity(spikes_file, settings, graph_title='Average activity', verbose=False):
        """
        Plots the average activity plot of a SpikesFile.

        This is, a graph where time is represented in the X axis, and average number of spikes in the Y axis.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                graph_title (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[ ] average_activity_L: Average activity array.
                int[ ] average_activity_R: Average activity array. Only returned if the mono_stereo parameter in settings is set to 1
        """
        # Convert to numpy array
        addresses = np.array(spikes_file.addresses, copy=False)
        timestamps = np.array(spikes_file.timestamps, copy=False)

        # Define plot variables
        total_time = np.max(timestamps)
        last_ts = 0
        mid_address = settings.num_channels * (settings.on_off_both + 1)
        num_bins = int(math.ceil(total_time / settings.bin_size))

        average_activity_L = np.zeros(num_bins)
        if settings.mono_stereo == 1:
            average_activity_R = np.zeros(num_bins)

        if verbose:
            start_time = time.time()

        # Array of bins
        bins = np.arange(num_bins) * settings.bin_size

        # Calculate the bin associated with each timestamp
        bins_indexes = np.digitize(timestamps, bins)

        # Cutting indexes (timestamps must be sorted)
        cut_indexes = np.where(np.diff(bins_indexes) > 0)[0]

        # Split timestamps by cutting indexes
        spikes_per_bins = np.array_split(addresses, cut_indexes)

        # Calculate the number of spikes in the bins
        for i in range(len(spikes_per_bins)):
            count_below = np.count_nonzero(spikes_per_bins[i] < mid_address)
            average_activity_L[i] = count_below
            if settings.mono_stereo == 1:
                average_activity_R[i] = len(spikes_per_bins[i]) - count_below

        if verbose:
            print('AVERAGE ACTIVITY CALCULATION', time.time() - start_time)

        plt.style.use('seaborn-whitegrid')
        avg_fig = plt.figure()
        avg_fig.canvas.set_window_title(graph_title)
        plt.title(graph_title, fontsize='x-large')
        plt.xlabel('Bin (' + str(settings.bin_size) + '$\mu$s width)', fontsize='large')
        plt.ylabel('No. of spikes', fontsize='large')

        plt.plot(bins / settings.bin_size, average_activity_L, label='Left cochlea', rasterized=True)
        if settings.mono_stereo == 1:
            plt.plot(bins / settings.bin_size, average_activity_R, label='Right cochlea')
            plt.legend(loc='best', ncol=2, frameon=True)

        plt.tight_layout()
        if settings.mono_stereo == 0:
            return average_activity_L, avg_fig
        else:
            return average_activity_L, average_activity_R, avg_fig

    @staticmethod
    def difference_between_LR(spikes_file, settings, return_data=False, graph_title='Diff. between L and R cochlea',
                              verbose=False, start_at_zero=True):
        """
        Plots a plot showing the differente between the left and the right activity of a SpikesFile.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                return_data (boolean, optional): When set to True, the sonogram matrix will be returned instead of plotted.
                graph_title (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.

        Returns:
                int[ , ]: Disparity matrix. Only returned if return_data is set to True.

        Raises:
                SettingsError: if settings.mono_stereo == 0

        Note:
                This function can only be called if the mono_stereo parameter in settings is set to 1.
        """
        if settings.mono_stereo == 1:
            if verbose:
                start_time = time.time()

            # Convert to numpy array
            timestamps = np.array(spikes_file.timestamps, copy=False)

            # Check start
            if start_at_zero:
                total_time = np.max(timestamps)
                last_time = 0
            else:
                min_timestamp = np.min(timestamps)
                total_time = np.max(timestamps) - min_timestamp
                last_time = min_timestamp

            # Calculate number of addresses and number of windows
            num_addresses = settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)
            mid_address = round(num_addresses / 2)
            num_windows = int(math.ceil(total_time / settings.bin_size))

            # Define diff array and partial arrays
            diff = np.zeros((round(num_addresses / 2), num_windows))

            if verbose:
                start_time = time.time()

            for i in range(num_windows):
                a = bisect_left(spikes_file.timestamps, last_time)
                b = bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

                blockAddr = spikes_file.addresses[a:b]

                spikes = np.bincount(blockAddr, minlength=num_addresses)

                diff[:, i] = spikes[0:mid_address] - spikes[mid_address:num_addresses]

                last_time += settings.bin_size

            if verbose:
                print('DIFF CALCULATION', time.time() - start_time)

            max_abs = np.max(abs(diff))
            if max_abs != 0:
                diff = diff * 100 / max_abs

            if not return_data:
                # REPRESENTATION
                plt.style.use('default')
                dlr_fig = plt.figure()
                dlr_fig.canvas.set_window_title(graph_title)

                # cmap = 'RdBu'
                colors = [(1, 0.49803921568627450980392156862745, 0.05490196078431372549019607843137), (1, 1, 1), (
                    0.12156862745098039215686274509804, 0.46666666666666666666666666666667,
                    0.70588235294117647058823529411765)]  # R -> G -> B
                n_bins = [3, 6, 10, 100]  # Discretizes the interpolation into bins
                cmap_name = 'my_list'
                cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

                plt.imshow(diff, vmin=-100, vmax=100, aspect="auto", cmap=cm, rasterized=True)  # , aspect="auto")
                plt.gca().invert_yaxis()

                plt.xlabel('Bin (' + str(settings.bin_size) + '$\mu$s width)', fontsize='large')
                plt.ylabel('Address', fontsize='large')

                plt.title(graph_title, fontsize='x-large')

                colorbar = plt.colorbar(ticks=[100, 50, 0, -50, -100], orientation='horizontal')
                colorbar.set_label('Cochlea predominance', rotation=0, fontsize='large', labelpad=10)
                colorbar.ax.set_xticklabels(['100% L\nCochlea', '50%', '0%\nL==R', '50%', '100% R\nCochlea'])
                colorbar.ax.invert_xaxis()

                return dlr_fig
            else:
                return diff
        else:
            # print("This functionality is only available for stereo AEDAT files.")
            print("[Plots.difference_between_LR] > SettingsError: This functionality is only available for stereo files.")

    @staticmethod
    def mso_heatmap(localization_file, localization_settings, graph_title="MSO heatmap", enable_colorbar=True,
                    verbose=False):
        """
        Plots the heatmap for the MSO activity extracted from a LocalizationFile.

        This is, a graph where the X axis means the neuron ID, the Y axis means the frequency channel to which the MSO neuron's population are connected, and the color means the activity.

        Parameters:
                localization_file (LocalizationFile): Localization file to plot.
                localization_settings (LocalizationSettings): Localization configuration parameters for the file to plot.
                graph_title (string, optional): Text that will appear as title for the graph.
                enable_colorbar (boolean, optional): Set to True if you want to show the color bar that indicates the activity range by colors.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note:
                None.
        """

        if verbose == True: start_time = time.time()

        # Get the number of frequency channels set in the configuration
        mso_number_freq_ch = localization_settings.mso_end_channel - localization_settings.mso_start_channel + 1

        # Create the activity matrix
        mso_activity = np.zeros((mso_number_freq_ch, localization_settings.mso_num_neurons_channel))

        num_mso_events = len(localization_file.mso_timestamps)

        for i in range(0, num_mso_events):
            # Move the frequency channel from the relative range to an absolute range starting at zero
            freq_channel = localization_file.mso_channels[i] - localization_settings.mso_start_channel
            neuron_id = localization_file.mso_neuron_ids[i]
            # Accumulate the activity for each neuron for each frequency channel according to the LocalizationFIle
            mso_activity[freq_channel][neuron_id] = mso_activity[freq_channel][neuron_id] + 1

        if verbose == True: print('MSO HEATMAP CALCULATION', time.time() - start_time)

        # Generate the labels lists
        freq_channel_labels = []
        for i in range(localization_settings.mso_start_channel, localization_settings.mso_end_channel + 1):
            freq_channel_labels.append(str(i))

        neuron_id_labels = []
        for i in range(0, localization_settings.mso_num_neurons_channel):
            neuron_id_labels.append(str(i))

        # REPRESENTATION
        plt.style.use('seaborn-ticks')
        htmap_fig, htmap_ax = plt.subplots()
        htmap_fig.canvas.set_window_title(graph_title)

        # Create the heatmap image
        htmap_im = plt.imshow(mso_activity, cmap='viridis')

        if enable_colorbar == True:
            colorbar = plt.colorbar()
            colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad=10)

        # Set the ticks
        htmap_ax.set_xticks(np.arange(len(neuron_id_labels)))
        htmap_ax.set_yticks(np.arange(len(freq_channel_labels)))
        # And set all the ticks' labels
        htmap_ax.set_xticklabels(neuron_id_labels)
        htmap_ax.set_yticklabels(freq_channel_labels)

        htmap_ax.set_xlabel('Neuron ID', fontsize='large')
        htmap_ax.set_ylabel('Freq. channel', fontsize='large')

        # Rotate the tick labels and set their alignment.
        plt.setp(htmap_ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(freq_channel_labels)):
            for j in range(len(neuron_id_labels)):
                text = htmap_ax.text(j, i, mso_activity[i, j],
                                     ha="center", va="center", color="w", fontsize='xx-small')

        plt.title(graph_title, fontsize='x-large')

        plt.tight_layout()
        htmap_fig.show()

    @staticmethod
    def mso_spikegram(localization_file, settings, localization_settings, dot_size=0.2, graph_title='MSO spikegram',
                      verbose=False):
        """
        Plots the 3D spikegram (also known as raster plot) of the MSO information contained in a LocalizationFile.
        This is, a graph where the X axis represents neuron IDs, the Y axis means time, and the Z axis represents the frequency channels of the cochlea, and where every spike is plotted as a dot.

        Parameters:
                localization_file (LocalizationFile): Localization file to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                localization_settings (LocalizationSettings): Localization configuration parameters for the file to plot.
                dot_size (float): Size of the dots used in the spikegram plot.
                graph_title (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note:
                None.
        """

        if verbose == True: start_time = time.time()

        # REPRESENTATION
        plt.style.use('seaborn-whitegrid')
        msospk_fig = plt.figure()
        ax = msospk_fig.add_subplot(111, projection='3d')
        msospk_fig.canvas.set_window_title(graph_title)

        # Plot all the spikes stored in the localization_file
        ax.scatter(localization_file.mso_neuron_ids, localization_file.mso_timestamps, localization_file.mso_channels,
                   s=dot_size)

        if verbose == True: print('MSO SPIKEGRAM CALCULATION', time.time() - start_time)

        plt.title(graph_title, fontsize='x-large')

        # Set the label of each axis
        ax.set_xlabel('Neuron ID', fontsize='large')
        ax.set_ylabel('Timestamp ($\mu$s)', fontsize='large')
        ax.set_zlabel('Freq. channel', fontsize='large')

        # Set the axis' limits for each axis according to the LocalizationSettings parameters
        ax.set_xlim([0, localization_settings.mso_num_neurons_channel])
        ax.set_ylim([0, localization_file.mso_timestamps[-1]])
        ax.set_zlim([0, settings.num_channels])

        plt.tight_layout()
        msospk_fig.show()

    @staticmethod
    def mso_localization_plot(localization_file, settings, localization_settings,
                              graph_title="MSO localization estimation", start_at_zero=True, verbose=False):
        """
        Plots the result of the coincidence counters of the Jeffress model for the MSO according to the activity in the LocalizationFile.

        This is, the neuron that fired the most in a time bin, thus indicating the sound source position.

        Parameters:
                localization_file (LocalizationFile): Localization file to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                localization_settings (LocalizationSettings): Localization configuration parameters for the file to plot.
                graph_title (string, optional): Text that will appear as title for the graph.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note:
                None.
        """

        if verbose == True: start_time = time.time()

        last_time = 0

        # Set the timestamps limits according to start_at_zero option
        if start_at_zero:
            total_time = max(localization_file.mso_timestamps)
            last_time = 0
        else:
            total_time = max(localization_file.mso_timestamps) - min(localization_file.mso_timestamps)
            last_time = min(localization_file.mso_timestamps)

        # Estimate the number of time bins
        its = int(math.ceil(total_time / settings.bin_size))

        # Create the activity array
        mso_activity = np.zeros((its, localization_settings.mso_num_neurons_channel))
        mso_max_activity = np.zeros(its)

        # For each time bin, calculate the activity of all the MSO neurons and get the winner
        for i in range(0, its):
            a = bisect_left(localization_file.mso_timestamps, last_time)
            b = bisect_right(localization_file.mso_timestamps, last_time + settings.bin_size)

            blockNeuronIDs = localization_file.mso_neuron_ids[a:b]

            spikes = np.bincount(blockNeuronIDs, minlength=localization_settings.mso_num_neurons_channel)

            last_time += settings.bin_size

            mso_activity[i, :] = spikes

            index_max_activity = np.argmax(mso_activity[i])

            mso_max_activity[i] = index_max_activity

        if verbose == True: print('MSO_LOCALIZATION PLOT CALCULATION', time.time() - start_time)

        # Set the figure
        plt.style.use('seaborn-whitegrid')
        mso_loc_fig = plt.figure()
        mso_loc_fig.canvas.set_window_title(graph_title)
        plt.title(graph_title, fontsize='x-large')
        plt.xlabel('Bin (' + str(settings.bin_size) + '$\mu$s width)', fontsize='large')
        plt.ylabel('Position (in degrees)', fontsize='large')
        plt.ylim([-1, localization_settings.mso_num_neurons_channel + 1])

        yticklabels = []
        angle_slot = 180.0 / localization_settings.mso_num_neurons_channel
        for slot_index in range(0, localization_settings.mso_num_neurons_channel):
            middle_angle = (slot_index * angle_slot) - 90.0 + (angle_slot / 2.0)
            yticklabels.append(str(int(abs(middle_angle))))

        plt.yticks(ticks=np.arange(localization_settings.mso_num_neurons_channel), labels=yticklabels, fontsize='small')

        plt.plot(np.arange(math.ceil(total_time / settings.bin_size)), mso_max_activity, label='Position estimation')

        # Add some text to clarify the results
        plt.annotate('Left side',
                     xy=(1.00, 0.85), xytext=(5, 0),
                     xycoords=('axes fraction', 'axes fraction'),
                     textcoords='offset points',
                     size=11, ha='center', va='center', rotation=270)

        plt.annotate('Centre',
                     xy=(1.00, 0.50), xytext=(5, 0),
                     xycoords=('axes fraction', 'axes fraction'),
                     textcoords='offset points',
                     size=11, ha='center', va='center', rotation=270)

        plt.annotate('Right side',
                     xy=(1.00, 0.15), xytext=(5, 0),
                     xycoords=('axes fraction', 'axes fraction'),
                     textcoords='offset points',
                     size=11, ha='center', va='center', rotation=270)

        plt.tight_layout()
        mso_loc_fig.show()

    @staticmethod
    def mso_histogram(localization_file, settings, localization_settings, graph_title='MSO histogram', verbose=False):
        """
        Plots the 3D histogram of the MSO information contained in a LocalizationFile.

        This is, a graph where neuron IDs are represented in the X axis, frequency channels are represented in the Y axis, and number of spikes in the Z axis.

        Parameters:
                localization_file (LocalizationFile): Localization file to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                localization_settings (LocalizationSettings): Localization configuration parameters for the file to plot.
                graph_title (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note:
                None.
        """

        start_time = time.time()

        # Set the total number of frequency channels
        mso_number_freq_ch = localization_settings.mso_end_channel - localization_settings.mso_start_channel + 1

        # Create the activity matrix
        mso_activity = np.zeros((mso_number_freq_ch, localization_settings.mso_num_neurons_channel))

        num_mso_events = len(localization_file.mso_timestamps)

        # Calculate the total number of events for each frequency channel and for each neuron ID
        for i in range(0, num_mso_events):
            freq_channel = localization_file.mso_channels[i] - localization_settings.mso_start_channel
            neuron_id = localization_file.mso_neuron_ids[i]
            # Accumulate the activity for each neuron for each frequency channel according to the LocalizationFIle
            mso_activity[freq_channel][neuron_id] = mso_activity[freq_channel][neuron_id] + 1

        if verbose == True: print('MSO HISTOGRAM CALCULATION:', time.time() - start_time)

        # Representation
        plt.style.use('seaborn-whitegrid')
        mso_hst_fig = plt.figure()
        ax = mso_hst_fig.add_subplot(111, projection='3d')

        # Set the data to show
        _x = np.arange(localization_settings.mso_num_neurons_channel)
        _y = np.arange(mso_number_freq_ch)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()
        z = mso_activity.ravel()

        top = z
        bottom = np.zeros_like(top)
        width = depth = 1

        ax.bar3d(x, y, bottom, width - 0.25, depth - 0.5, top, shade=True)
        ax.set_title('Shaded')

        # Set the axes' limits
        ax.set_xlim3d(0, localization_settings.mso_num_neurons_channel)
        ax.set_ylim3d(0, mso_number_freq_ch)
        ax.set_zlim3d(0, np.amax(z))

        # Set the axes' labels
        ax.set_xlabel('Neuron ID', fontsize='large')
        ax.set_ylabel('Freq. channel', fontsize='large')
        ax.set_zlabel('No. of spikes', fontsize='large')

        # Generate the labels lists
        freq_channel_labels = []
        for i in range(localization_settings.mso_start_channel, localization_settings.mso_end_channel + 1):
            freq_channel_labels.append(str(i))

        # Set all the ticks
        ax.set_yticks(np.arange(len(freq_channel_labels)))
        # And all the ticks' labels
        ax.set_yticklabels(freq_channel_labels)

        mso_hst_fig.canvas.set_window_title(graph_title)
        plt.title(graph_title, fontsize='x-large')

        mso_hst_fig.show()
