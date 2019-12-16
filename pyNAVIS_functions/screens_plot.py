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
#import struct

import random
#import collections

import matplotlib.pyplot as plt
import numpy as np

from bisect import bisect_left, bisect_right
from pyNAVIS_functions.utils import *

def spikegram(spikes_file, settings, graph_tile = 'Spikegram', verbose = False):

    if verbose == True: start_time = time.time()
    #REPRESENTATION
    plt.style.use('seaborn-whitegrid')
    spk_fig = plt.figure()
    spk_fig.canvas.set_window_title(graph_tile)

    random.seed('just some random seed')

    if settings.mono_stereo == 0:
        plt.scatter(spikes_file.timestamps[0::settings.spikegram_dot_freq], spikes_file.addresses[0::settings.spikegram_dot_freq], s=settings.spikegram_dot_size)
    else:
        aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] < settings.num_channels*(settings.on_off_both)])
        plt.scatter(ts[0::settings.spikegram_dot_freq], addr[0::settings.spikegram_dot_freq], s=settings.spikegram_dot_size, label='Left cochlea')
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] >= settings.num_channels*(settings.on_off_both) and evt[0] < settings.num_channels*(settings.on_off_both)*2])
        plt.scatter(ts[0::settings.spikegram_dot_freq], addr[0::settings.spikegram_dot_freq], s=settings.spikegram_dot_size, label='Right cochlea')
        plt.legend(fancybox=False, ncol=2, loc='upper center', markerscale=2/settings.spikegram_dot_size, frameon=True)
        
    if verbose == True: print('SPIKEGRAM CALCULATION', time.time() - start_time)

    plt.title('Spikegram', fontsize='x-large')
    plt.xlabel('Timestamp ($\mu$s)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    spk_fig.show()


def sonogram(spikes_file, settings, return_data = False, verbose = False):
    
    if verbose == True: start_time = time.time()

    total_time = max(spikes_file.timestamps) - min(spikes_file.timestamps)

    sonogram = np.zeros((settings.num_channels*2*(settings.mono_stereo+1), int(math.ceil(total_time/settings.bin_size))))

    last_time = min(spikes_file.timestamps)

    its = int(math.ceil(total_time/settings.bin_size))
    
    #THIS IS NOT NEEDED IF TS ARE SORTED
    aedat_addr_ts = zip(spikes_file.addresses, spikes_file.timestamps)
    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    spikes_file = extract_addr_and_ts(aedat_addr_ts)
    
    for i in range(its):

        a =  bisect_left(spikes_file.timestamps, last_time)
        b =  bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

        blockAddr = spikes_file.addresses[a:b]

        spikes = np.bincount(blockAddr, minlength=settings.num_channels*2*(settings.mono_stereo+1))        

        last_time += settings.bin_size
        sonogram[:, i] = spikes

    if verbose == True: print('SONOGRAM CALCULATION', time.time() - start_time)
    
    if return_data == False:
        # REPRESENTATION
        plt.style.use('default')
        sng_fig = plt.figure()
        sng_fig.canvas.set_window_title('Sonogram')

        plt.imshow(sonogram, aspect="auto") #, aspect="auto")
        plt.gca().invert_yaxis()

        plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
        plt.ylabel('Address', fontsize='large')

        plt.title('Sonogram', fontsize='x-large')

        colorbar = plt.colorbar()
        colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad= 10) #, rotation=270)

        sng_fig.show()
    else:
        return sonogram


def histogram(spikes_file, settings, verbose = False):
    start_time = time.time()
    spikes_count = np.bincount(spikes_file.addresses)
    if verbose == True: print('TIEMPO HISTOGRAM:', time.time() - start_time)

    plt.style.use('seaborn-whitegrid')
    hst_fig = plt.figure()
    hst_fig.canvas.set_window_title('Histogram')
    plt.title('Histogram', fontsize='x-large')
    plt.xlabel('Address', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    if settings.bar_line == 0:
        if settings.mono_stereo == 1:
            plt.bar(np.arange(settings.num_channels * 2), spikes_count[0:settings.num_channels*2])
            plt.bar(np.arange(settings.num_channels * 2), spikes_count[settings.num_channels*2:settings.num_channels*4])
        else:
            plt.bar(np.arange(settings.num_channels * 2 * (settings.mono_stereo + 1)), spikes_count)
    else:
        if settings.mono_stereo == 1:
            plt.plot(np.arange(settings.num_channels * 2), spikes_count[0:settings.num_channels*2], label='Left cochlea')
            plt.plot(np.arange(settings.num_channels * 2), spikes_count[settings.num_channels*2:settings.num_channels*4], label='Right cochlea')
            plt.legend(loc='best', frameon=True)
        else:
            plt.plot(np.arange(settings.num_channels * 2 * (settings.mono_stereo + 1)), spikes_count)

    hst_fig.show()


def average_activity(spikes_file, settings, verbose=False):
    aedat_addr_ts = zip(spikes_file.addresses, spikes_file.timestamps)
    total_time = int(max(spikes_file.timestamps))
    last_ts = 0
    average_activity_L = np.zeros(int(math.ceil(total_time/settings.bin_size))+1)
    if(settings.mono_stereo == 1):
        average_activity_R = np.zeros(int(math.ceil(total_time/settings.bin_size))+1)

    #THIS TWO ONLY IF CHECK DETECTS AEDAT NOT IN ORDER
    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    spikes_file = extract_addr_and_ts(aedat_addr_ts)

    if verbose == True: start_time = time.time()
    if settings.mono_stereo == 1: 
        for i in range(0, total_time, settings.bin_size):        
            evtL = 0
            evtR = 0

            a =  bisect_left(spikes_file.timestamps, last_ts)
            b =  bisect_right(spikes_file.timestamps, last_ts + settings.bin_size)

            events_list = spikes_file.addresses[a:b]
            
            for j in events_list:
                if j < settings.num_channels*2:
                    evtL = evtL + 1
                elif j >= settings.num_channels*2 and j < settings.num_channels*2*2:
                    evtR = evtR + 1

            average_activity_L[i/settings.bin_size] = evtL
            average_activity_R[i/settings.bin_size] = evtR
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
    avg_fig.canvas.set_window_title('Average activity')
    plt.title('Average activity', fontsize='x-large')
    plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    plt.plot(np.arange(math.ceil(total_time/settings.bin_size)+1), average_activity_L, label='Left cochlea')
    if(settings.mono_stereo == 1):
        plt.plot(np.arange(math.ceil(total_time/settings.bin_size)+1), average_activity_R, label='Right cochlea')
        plt.legend(loc='best',  ncol=2, frameon=True)
    avg_fig.show()


def difference_between_LR(spikes_file, settings, verbose = False):
    if settings.mono_stereo == 1:    
        total_time = max(spikes_file.timestamps) - min(spikes_file.timestamps)
        diff = np.zeros((settings.num_channels*settings.on_off_both, int(math.ceil(total_time/settings.bin_size))))

        last_time = min(spikes_file.timestamps)

        its = int(math.ceil(total_time/settings.bin_size))

        #THIS IS NOT NEEDED IF TS ARE SORTED
        aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
        aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
        spikes_file = extract_addr_and_ts(aedat_addr_ts)

        if verbose == True: start_time = time.time()
        for i in range(its):
            a =  bisect_left(spikes_file.timestamps, last_time)
            b =  bisect_right(spikes_file.timestamps, last_time + settings.bin_size)

            blockAddr = spikes_file.addresses[a:b]
            
            spikes = np.bincount(blockAddr, minlength=settings.num_channels*settings.on_off_both*(settings.mono_stereo+1))
            
            last_time += settings.bin_size

            diff[:, i] = [x1 - x2 for (x1, x2) in list(zip(spikes[0:settings.num_channels*settings.on_off_both], spikes[settings.num_channels*settings.on_off_both:settings.num_channels*settings.on_off_both*2]))]
        if verbose == True: print('DIFF CALCULATION', time.time() - start_time)
        
        if max(abs(np.min(diff)), np.max(diff)) != 0: diff = diff*100/max(abs(np.min(diff)), np.max(diff))

        # REPRESENTATION
        plt.style.use('default')
        sng_fig = plt.figure()
        sng_fig.canvas.set_window_title('Diff. between L and R cochlea')

        plt.imshow(diff, vmin=-100, vmax=100, aspect="auto") #, aspect="auto")
        plt.gca().invert_yaxis()

        plt.xlabel('Bin ('+str(settings.bin_size) + '$\mu$s width)', fontsize='large')
        plt.ylabel('Address', fontsize='large')

        plt.title('Diff. between L and R cochlea', fontsize='x-large')

        colorbar = plt.colorbar(ticks=[100, 50, 0, -50, -100], orientation='horizontal')
        colorbar.set_label('Cochlea predominance', rotation=0, fontsize='large', labelpad= 10)
        colorbar.ax.set_xticklabels(['100% L cochlea', '50%', '0% L==R', '50%', '100% R cochlea'])
        colorbar.ax.invert_xaxis()
        sng_fig.show()
    else:
        print("This functionality is only available for stereo AER-DATA files.")