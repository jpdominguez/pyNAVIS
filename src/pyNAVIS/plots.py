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
from bisect import bisect_left, bisect_right
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.pyplot as plt
import numpy as np
import time

from .utils import Utils

class Plots:
    @staticmethod
    def spikegram(spikes_file, settings, dot_size = 0.2, dot_freq = 1, graph_tile = 'Spikegram', start_at_zero = True, verbose = False):
        """
        Plots the spikegram (also known as cochleogram or raster plot) of a SpikesFile.
        
        This is, a graph where the X axis means time and the Y axis represents addresses (or cochlea channels), and where every spike is plotted as a dot.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                dot_size (float): Size of the dots used in the spikegram plot.
                dot_freq (int): Set the frequency of spikes that will be represented in the spikegram.
                graph_tile (string, optional): Text that will appear as title for the graph.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.

        Note: 
                A value of 10 in dot_size means that for every 10 spikes, only 1 will be plotted. This helps reducing lag when plotting heavy files.
        """

        if verbose == True: start_time = time.time()
        #REPRESENTATION
        plt.style.use('seaborn-whitegrid')
        spk_fig = plt.figure()
        spk_fig.canvas.set_window_title(graph_tile)

        random.seed(0)

        if settings.mono_stereo == 0:
            plt.scatter(spikes_file.timestamps[0::dot_freq], spikes_file.addresses[0::dot_freq], s=dot_size)
        else:
            aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
            addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] < settings.num_channels*(settings.on_off_both + 1)])
            plt.scatter(ts[0::dot_freq], addr[0::dot_freq], s=dot_size, label='Left cochlea')
            addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] >= settings.num_channels*(settings.on_off_both + 1) and evt[0] < settings.num_channels*(settings.on_off_both + 1)*2])
            plt.scatter(ts[0::dot_freq], addr[0::dot_freq], s=dot_size, label='Right cochlea')
            plt.legend(fancybox=False, ncol=2, loc='upper center', markerscale=2/dot_size, frameon=True)
            
        if verbose == True: print('SPIKEGRAM CALCULATION', time.time() - start_time)

        plt.title(graph_tile, fontsize='x-large')
        plt.xlabel('Timestamp ($\mu$s)', fontsize='large')
        plt.ylabel('Address', fontsize='large')
        plt.ylim([0, settings.num_channels*(settings.on_off_both + 1)*(settings.mono_stereo + 1)])

        if start_at_zero:
            plt.xlim([0, np.max(spikes_file.timestamps)])

        plt.tight_layout()
        spk_fig.show()

    @staticmethod
    def sonogram(spikes_file, settings, return_data = False, graph_tile = 'Sonogram', start_at_zero = True, verbose = False):
        """
        Plots the sonogram of a SpikesFile.
        
        This is, a graph where the X axis means time and the Y axis represents addresses (or cochlea channels), and where the spiking activity is shown with color.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                return_data (boolean, optional): When set to True, the sonogram matrix will be returned instead of plotted.
                graph_tile (string, optional): Text that will appear as title for the graph.
                start_at_zero (boolean, optional): If set to True, the X axis will start at 0, instead of starting at the minimum timestamp.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[ , ]: Sonogram matrix. Only returned if return_data is set to True.
        """
        if verbose == True: start_time = time.time()

        if start_at_zero:
            total_time = max(spikes_file.timestamps)
            last_time = 0
        else:
            total_time = max(spikes_file.timestamps) - min(spikes_file.timestamps)
            last_time = min(spikes_file.timestamps)
        

        sonogram = np.zeros((settings.num_channels*(settings.on_off_both + 1)*(settings.mono_stereo+1), int(math.ceil(total_time/settings.bin_size))))

        its = int(math.ceil(total_time/settings.bin_size))
        
        #THIS IS NOT NEEDED IF TS ARE SORTED
        aedat_addr_ts = zip(spikes_file.addresses, spikes_file.timestamps)
        aedat_addr_ts = sorted(aedat_addr_ts, key=Utils.getKey)
        spikes_file = Utils.extract_addr_and_ts(aedat_addr_ts)
        
        for i in range(its):

            a =  bisect_left(spikes_file.timestamps, last_time)
            b =  bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

            blockAddr = spikes_file.addresses[a:b]

            spikes = np.bincount(blockAddr, minlength=settings.num_channels*(settings.on_off_both + 1)*(settings.mono_stereo+1))        

            last_time += settings.bin_size
            sonogram[:, i] = spikes

        if verbose == True: print('SONOGRAM CALCULATION', time.time() - start_time)
        
        if return_data == False:
            # REPRESENTATION
            plt.style.use('default')
            sng_fig = plt.figure()
            sng_fig.canvas.set_window_title(graph_tile)

            plt.imshow(sonogram, aspect="auto", cmap='hot') #, aspect="auto")
            plt.gca().invert_yaxis()

            plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
            plt.ylabel('Address', fontsize='large')

            plt.title(graph_tile, fontsize='x-large')

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
            colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad= 10)

            sng_fig.show()
        else:
            return sonogram


    @staticmethod
    def histogram(spikes_file, settings, bar_line = 1, graph_tile = 'Histogram', verbose = False):
        """
        Plots the histogram of a SpikesFile.
        
        This is, a graph where addresses (or cochlea channels) are represented in the X axis, and number of spikes in the Y axis.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                bar_line (int, optional): Select wether to plot the histogram as bar plot (0) or as a line graph (1).
                graph_tile (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[]: Histogram array.
        """

        start_time = time.time()
        
        spikes_count = np.bincount(spikes_file.addresses, minlength=settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1))

        if verbose == True: print('HISTOGRAM CALCULATION:', time.time() - start_time)

        plt.style.use('seaborn-whitegrid')
        hst_fig = plt.figure()
        hst_fig.canvas.set_window_title(graph_tile)
        plt.title(graph_tile, fontsize='x-large')
        plt.xlabel('Address', fontsize='large')
        plt.ylabel('No. of spikes', fontsize='large')

        if bar_line == 0:
            if settings.mono_stereo == 1:
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1)), spikes_count[0:settings.num_channels*(settings.on_off_both + 1)])
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1)), spikes_count[settings.num_channels*(settings.on_off_both + 1):settings.num_channels*2*(settings.on_off_both + 1)])
            else:
                plt.bar(np.arange(settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)), spikes_count)
        else:
            if settings.mono_stereo == 1:
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1)), spikes_count[0:settings.num_channels*(settings.on_off_both + 1)], label='Left cochlea')
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1)), spikes_count[settings.num_channels*(settings.on_off_both + 1):settings.num_channels*2*(settings.on_off_both + 1)], label='Right cochlea')
                plt.legend(loc='best', frameon=True)
            else:
                plt.plot(np.arange(settings.num_channels * (settings.on_off_both + 1) * (settings.mono_stereo + 1)), spikes_count)

        plt.tight_layout()
        hst_fig.show()
        return spikes_count

    @staticmethod
    def average_activity(spikes_file, settings, graph_tile = 'Average activity', verbose=False):
        """
        Plots the average activity plot of a SpikesFile.
        
        This is, a graph where time is represented in the X axis, and average number of spikes in the Y axis.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                graph_tile (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """
        aedat_addr_ts = zip(spikes_file.addresses, spikes_file.timestamps)
        total_time = int(max(spikes_file.timestamps))
        last_ts = 0
        average_activity_L = np.zeros(int(math.ceil(total_time/settings.bin_size))+1)
        if(settings.mono_stereo == 1):
            average_activity_R = np.zeros(int(math.ceil(total_time/settings.bin_size))+1)

        #THIS TWO ONLY IF CHECK DETECTS AEDAT NOT IN ORDER
        aedat_addr_ts = sorted(aedat_addr_ts, key=Utils.getKey)
        spikes_file = Utils.extract_addr_and_ts(aedat_addr_ts)

        if verbose == True: start_time = time.time()
        if settings.mono_stereo == 1: 
            for i in range(0, total_time, settings.bin_size):        
                evtL = 0
                evtR = 0

                a =  bisect_left(spikes_file.timestamps, last_ts)
                b =  bisect_right(spikes_file.timestamps, last_ts + settings.bin_size)

                events_list = spikes_file.addresses[a:b]
                
                for j in events_list:
                    if j < settings.num_channels*(1 + settings.on_off_both):
                        evtL = evtL + 1
                    elif j >= settings.num_channels*(1 + settings.on_off_both) and j < settings.num_channels*(1 + settings.on_off_both)*2:
                        evtR = evtR + 1

                average_activity_L[int(i/settings.bin_size)] = evtL
                average_activity_R[int(i/settings.bin_size)] = evtR
                last_ts = last_ts + settings.bin_size
        elif settings.mono_stereo == 0:
            for i in range(0, total_time, settings.bin_size):
                evtL = 0

                a =  bisect_left(spikes_file.timestamps, last_ts)
                b =  bisect_right(spikes_file.timestamps, last_ts + settings.bin_size)
                events_list = spikes_file.addresses[a:b]
                
                for j in events_list:
                    evtL = evtL + 1

                average_activity_L[i//settings.bin_size] = evtL
                last_ts = last_ts + settings.bin_size
        if verbose == True: print('AVERAGE ACTIVITY CALCULATION', time.time() - start_time)

        plt.style.use('seaborn-whitegrid')
        avg_fig = plt.figure()
        avg_fig.canvas.set_window_title(graph_tile)
        plt.title(graph_tile, fontsize='x-large')
        plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
        plt.ylabel('No. of spikes', fontsize='large')

        plt.plot(np.arange(math.ceil(total_time/settings.bin_size)+1), average_activity_L, label='Left cochlea')
        if(settings.mono_stereo == 1):
            plt.plot(np.arange(math.ceil(total_time/settings.bin_size)+1), average_activity_R, label='Right cochlea')
            plt.legend(loc='best',  ncol=2, frameon=True)

        plt.tight_layout()
        avg_fig.show()

    @staticmethod
    def difference_between_LR(spikes_file, settings, return_data = False, graph_tile = 'Diff. between L and R cochlea', verbose = False):
        """
        Plots a plot showing the differente between the left and the right activity of a SpikesFile.

        Parameters:
                spikes_file (SpikesFile): File to plot.
                settings (MainSettings): Configuration parameters for the file to plot.
                return_data (boolean, optional): When set to True, the sonogram matrix will be returned instead of plotted.
                graph_tile (string, optional): Text that will appear as title for the graph.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                int[ , ]: Disparity matrix. Only returned if return_data is set to True.

        Raises:
                SettingsError: if settings.mono_stereo == 0

        Note:
                This function can only be called if the mono_stereo parameter in settings is set to 1.
        """
        if settings.mono_stereo == 1:    
            total_time = max(spikes_file.timestamps) - min(spikes_file.timestamps)
            diff = np.zeros((settings.num_channels*(settings.on_off_both + 1), int(math.ceil(total_time/settings.bin_size))))

            last_time = min(spikes_file.timestamps)

            its = int(math.ceil(total_time/settings.bin_size))

            #THIS IS NOT NEEDED IF TS ARE SORTED
            aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
            aedat_addr_ts = sorted(aedat_addr_ts, key=Utils.getKey)
            spikes_file = Utils.extract_addr_and_ts(aedat_addr_ts)

            if verbose == True: start_time = time.time()
            for i in range(its):
                a =  bisect_left(spikes_file.timestamps, last_time)
                b =  bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

                blockAddr = spikes_file.addresses[a:b]
                
                spikes = np.bincount(blockAddr, minlength=settings.num_channels*(settings.on_off_both + 1)*(settings.mono_stereo+1))
                
                last_time += settings.bin_size

                diff[:, i] = [x1 - x2 for (x1, x2) in list(zip(spikes[0:settings.num_channels*(settings.on_off_both + 1)], spikes[settings.num_channels*(settings.on_off_both + 1):settings.num_channels*(settings.on_off_both + 1)*2]))]
            if verbose == True: print('DIFF CALCULATION', time.time() - start_time)
            
            if max(abs(np.min(diff)), np.max(diff)) != 0: diff = diff*100/max(abs(np.min(diff)), np.max(diff))

            if return_data == False:
                # REPRESENTATION
                plt.style.use('default')
                sng_fig = plt.figure()
                sng_fig.canvas.set_window_title(graph_tile)
                
                #cmap = 'RdBu'
                colors = [(1, 0.49803921568627450980392156862745, 0.05490196078431372549019607843137), (1, 1, 1), (0.12156862745098039215686274509804, 0.46666666666666666666666666666667, 0.70588235294117647058823529411765)]  # R -> G -> B
                n_bins = [3, 6, 10, 100]  # Discretizes the interpolation into bins
                cmap_name = 'my_list'
                cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

                plt.imshow(diff, vmin=-100, vmax=100, aspect="auto", cmap=cm) #, aspect="auto")
                plt.gca().invert_yaxis()

                plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
                plt.ylabel('Address', fontsize='large')

                plt.title(graph_tile, fontsize='x-large')

                colorbar = plt.colorbar(ticks=[100, 50, 0, -50, -100], orientation='horizontal')
                colorbar.set_label('Cochlea predominance', rotation=0, fontsize='large', labelpad= 10)
                colorbar.ax.set_xticklabels(['100% L\nCochlea', '50%', '0%\nL==R', '50%', '100% R\nCochlea'])
                colorbar.ax.invert_xaxis()
                sng_fig.show()
            else:
                return diff
        else:
            #print("This functionality is only available for stereo AEDAT files.")
            print("[Plots.difference_between_LR] > SettingsError: This functionality is only available for stereo files.")
