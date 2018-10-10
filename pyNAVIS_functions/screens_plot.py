import math
import struct

import random
import collections

import matplotlib.pyplot as plt
import numpy as np

from bisect import bisect_left, bisect_right
from pyNAVIS_functions.utils import *



def spikegram(allAddr, allTs, p_settings):

    #REPRESENTATION
    plt.style.use('seaborn-whitegrid')
    spk_fig = plt.figure()
    spk_fig.canvas.set_window_title('Spikegram')

    random.seed('just some random seed')

    if p_settings.mono_stereo == 0:
        #plt.scatter(random.sample(allTs, len(allAddr)/p_settings.spikegram_dot_freq), random.sample(allAddr, len(allAddr)/p_settings.spikegram_dot_freq), s=p_settings.spikegram_dot_size)
        plt.scatter(allTs[0::p_settings.spikegram_dot_freq], allAddr[0::p_settings.spikegram_dot_freq], s=p_settings.spikegram_dot_size)
    else:
        aedat_addr_ts = zip(allAddr, allTs)
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] < p_settings.num_channels*(p_settings.on_off_both)])
        plt.scatter(ts[0::p_settings.spikegram_dot_freq], addr[0::p_settings.spikegram_dot_freq], s=p_settings.spikegram_dot_size, label='Left cochlea')
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] >= p_settings.num_channels*(p_settings.on_off_both) and evt[0] < p_settings.num_channels*(p_settings.on_off_both)*2])
        plt.scatter(ts[0::p_settings.spikegram_dot_freq], addr[0::p_settings.spikegram_dot_freq], s=p_settings.spikegram_dot_size, label='Right cochlea')
        plt.legend(fancybox=False, ncol=2, loc='upper center', markerscale=2/p_settings.spikegram_dot_size, frameon=True)
        
    plt.title('Spikegram', fontsize='x-large')

    plt.xlabel('Timestamp ($\mu$s)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    spk_fig.show()


def sonogram(allAddr, allTs, p_settings):
    
    start_time = time.time()
    total_time = max(allTs) - min(allTs)

    sonogram = np.zeros((p_settings.num_channels*2*(p_settings.mono_stereo+1), int(math.ceil(total_time/p_settings.bin_size))))

    last_time = min(allTs)

    its = int(math.ceil(total_time/p_settings.bin_size))
    
    #THIS IS NOT NEEDED IF TS ARE SORTED
    aedat_addr_ts = zip(allAddr, allTs)
    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    allAddr, allTs = extract_addr_and_ts(aedat_addr_ts)
    
    
    for i in range(its):

        a =  bisect_left(allTs, last_time)
        b =  bisect_right(allTs, last_time + p_settings.bin_size)

        blockAddr = allAddr[a:b]

        spikes = np.bincount(blockAddr, minlength=p_settings.num_channels*2*(p_settings.mono_stereo+1))        

        last_time += p_settings.bin_size
        sonogram[:, i] = spikes

    print 'SONOGRAM CALCULATION', time.time() - start_time

    
    # REPRESENTATION
    plt.style.use('default')
    sng_fig = plt.figure()
    sng_fig.canvas.set_window_title('Sonogram')

    plt.imshow(sonogram) #, aspect="auto")
    plt.gca().invert_yaxis()

    plt.xlabel('Bin ('+str(p_settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    plt.title('Sonogram', fontsize='x-large')

    colorbar = plt.colorbar()
    colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad= 10) #, rotation=270)

    sng_fig.show()


def sonogram_debug(allAddr, allTs, p_settings):

    start_time = time.time()
    aedat_addr_ts = zip(allAddr, allTs)
    print 'ZIP:', time.time() - start_time

    start_time = time.time()
    total_time = max(allTs) - min(allTs)
    print 'MAX - MIN:', time.time() - start_time

    start_time = time.time()
    sonogram = np.zeros((p_settings.num_channels*2*(p_settings.mono_stereo+1), int(math.ceil(total_time/p_settings.bin_size))))
    print 'CREATE MATRIX', time.time() - start_time

    #last_time = aedat_addr_ts[0][1]
    last_time = min(allTs)

    its = int(math.ceil(total_time/p_settings.bin_size))

    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    allAddr, allTs = extract_addr_and_ts(aedat_addr_ts)

    for i in range(its):
        """
        start_time = time.time()
        blockAddr = [item[0] for item in aedat_addr_ts if item[1] >= last_time and item[1] < (last_time + p_settings.bin_size)]
        print 'BLOCK ADDR', time.time() - start_time
        """

        start_time = time.time()
        a =  bisect_left(allTs, last_time)
        b =  bisect_right(allTs, last_time + p_settings.bin_size)

        blockAddr = allAddr[a:b]
        print 'BLOCK ADDR_new', time.time() - start_time

        start_time = time.time()
        spikes = np.bincount(blockAddr, minlength=p_settings.num_channels*2*(p_settings.mono_stereo+1))        
        print 'FREQ', time.time() - start_time

        start_time = time.time()
        last_time += p_settings.bin_size
        sonogram[:, i] = spikes

        print 'INC LAST TIME + ADD COLUMN TO SONOGRAM', time.time() - start_time

    
    # REPRESENTATION
    plt.style.use('default')
    sng_fig = plt.figure()
    sng_fig.canvas.set_window_title('Sonogram')

    plt.imshow(sonogram) #, aspect="auto")
    plt.gca().invert_yaxis()

    plt.xlabel('Bin ('+str(p_settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    plt.title('Sonogram', fontsize='x-large')

    colorbar = plt.colorbar()
    colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad= 10) #, rotation=270)

    sng_fig.show()


def histogram(allAddr, p_settings):

    start_time = time.time()
    spikes_count = np.bincount(allAddr)
    print 'TIEMPO HISTOGRAM:', time.time() - start_time


    plt.style.use('seaborn-whitegrid')
    hst_fig = plt.figure()
    hst_fig.canvas.set_window_title('Histogram')
    plt.title('Histogram', fontsize='x-large')
    plt.xlabel('Address', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    if p_settings.bar_line == 0:
        if p_settings.mono_stereo == 1:
            plt.bar(np.arange(p_settings.num_channels * 2), spikes_count[0:p_settings.num_channels*2])
            plt.bar(np.arange(p_settings.num_channels * 2), spikes_count[p_settings.num_channels*2:p_settings.num_channels*4])
        else:
            plt.bar(np.arange(p_settings.num_channels * 2 * (p_settings.mono_stereo + 1)), spikes_count)
    else:
        if p_settings.mono_stereo == 1:
            plt.plot(np.arange(p_settings.num_channels * 2), spikes_count[0:p_settings.num_channels*2], label='Left cochlea')
            plt.plot(np.arange(p_settings.num_channels * 2), spikes_count[p_settings.num_channels*2:p_settings.num_channels*4], label='Right cochlea')
            plt.legend(loc='best', frameon=True)
        else:
            plt.plot(np.arange(p_settings.num_channels * 2 * (p_settings.mono_stereo + 1)), spikes_count)

    hst_fig.show()

def average_activity(allAddr, allTs, p_settings):
    aedat_addr_ts = zip(allAddr, allTs)
    total_time = int(max(allTs))
    last_ts = 0
    average_activity_L = np.zeros(int(math.ceil(total_time/p_settings.bin_size))+1)
    if(p_settings.mono_stereo == 1):
        average_activity_R = np.zeros(int(math.ceil(total_time/p_settings.bin_size))+1)


    #THIS TWO ONLY IF CHECK DETECTS AEDAT NOT IN ORDER
    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    allAddr, allTs = extract_addr_and_ts(aedat_addr_ts)

    if p_settings.mono_stereo == 1: 
        for i in range(0, total_time, p_settings.bin_size):        
            evtL = 0
            evtR = 0
            """
            events_list = [evt[0] for evt in aedat_addr_ts if (evt[1] >= last_ts and evt[1] < last_ts + p_settings.bin_size)]

            """
            a =  bisect_left(allTs, last_ts)
            b =  bisect_right(allTs, last_ts + p_settings.bin_size)

            events_list = allAddr[a:b]

            
            for j in events_list:
                if j < p_settings.num_channels*2:
                    evtL = evtL + 1
                elif j >= p_settings.num_channels*2 and j < p_settings.num_channels*2*2:
                    evtR = evtR + 1

            average_activity_L[i/p_settings.bin_size] = evtL
            average_activity_R[i/p_settings.bin_size] = evtR
            last_ts = last_ts + p_settings.bin_size
    elif p_settings.mono_stereo == 0:
        for i in range(0, total_time, p_settings.bin_size):
            evtL = 0
            """
            events_list = [evt[0] for evt in aedat_addr_ts if (evt[1] >= last_ts and evt[1] < last_ts + p_settings.bin_size)]
            """
            a =  bisect_left(allTs, last_ts)
            b =  bisect_right(allTs, last_ts + p_settings.bin_size)
            events_list = allAddr[a:b]
            
            for j in events_list:
                evtL = evtL + 1

            average_activity_L[i/p_settings.bin_size] = evtL
            last_ts = last_ts + p_settings.bin_size
        """
        spikes_between_timestamps_L = [evt[1] for evt in aedat_addr_ts if (evt[1] >= last_ts and evt[1] < last_ts + p_settings.bin_size) and evt[0] < p_settings.num_channels*2]
        average_activity_L[int(i/p_settings.bin_size)] = len(spikes_between_timestamps_L)
        if(p_settings.mono_stereo == 1):
            spikes_between_timestamps_R = [evt[1] for evt in aedat_addr_ts if (evt[1] >= last_ts and evt[1] < last_ts + p_settings.bin_size) and (evt[0] >= p_settings.num_channels*2 and evt[0] < p_settings.num_channels*2*2)]
            average_activity_R[int(i/p_settings.bin_size)] = len(spikes_between_timestamps_R)
        last_ts = last_ts + p_settings.bin_size
        """

    plt.style.use('seaborn-whitegrid')
    avg_fig = plt.figure()
    avg_fig.canvas.set_window_title('Average activity')
    plt.title('Average activity', fontsize='x-large')
    plt.xlabel('Bin ('+str(p_settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    plt.plot(np.arange(math.ceil(total_time/p_settings.bin_size)+1), average_activity_L, label='Left cochlea')
    if(p_settings.mono_stereo == 1):
        plt.plot(np.arange(math.ceil(total_time/p_settings.bin_size)+1), average_activity_R, label='Right cochlea')
        plt.legend(loc='best',  ncol=2, frameon=True)
    avg_fig.show()


def difference_between_LR(allAddr, allTs, p_settings):    
    total_time = max(allTs) - min(allTs)
    diff = np.zeros((p_settings.num_channels*2, int(math.ceil(total_time/p_settings.bin_size))))

    #spikes = [0] * p_settings.num_channels*2*2
    last_time = min(allTs)

    its = int(math.ceil(total_time/p_settings.bin_size))

    #THIS IS NOT NEEDED IF TS ARE SORTED
    aedat_addr_ts = zip(allAddr, allTs)
    aedat_addr_ts = sorted(aedat_addr_ts, key=getKey)
    allAddr, allTs = extract_addr_and_ts(aedat_addr_ts)

    start_time = time.time()
    for i in range(its):

        #blockAddr = [item[0] for item in aedat_addr_ts if item[1] >= last_time and item[1] < (last_time + p_settings.bin_size)]
        a =  bisect_left(allTs, last_time)
        b =  bisect_right(allTs, last_time + p_settings.bin_size)

        blockAddr = allAddr[a:b]
        
        spikes = np.bincount(blockAddr, minlength=p_settings.num_channels*2*(p_settings.mono_stereo+1))
        
        last_time += p_settings.bin_size

        diff[:, i] = [x1 - x2 for (x1, x2) in zip(spikes[0:p_settings.num_channels*2], spikes[p_settings.num_channels*2:p_settings.num_channels*2*2])]
    print 'DIFF CALCULATION', time.time() - start_time
    diff = diff*100/max(abs(np.min(diff)), np.max(diff))
    
    # REPRESENTATION
    plt.style.use('default')
    sng_fig = plt.figure()
    sng_fig.canvas.set_window_title('Diff. between L and R cochlea')

    plt.imshow(diff, vmin=-100, vmax=100) #, aspect="auto")
    plt.gca().invert_yaxis()

    plt.xlabel('Bin ('+str(p_settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    plt.title('Diff. between L and R cochlea', fontsize='x-large')

    colorbar = plt.colorbar(ticks=[100, 50, 0, -50, -100], orientation='horizontal')
    colorbar.set_label('Cochlea predominance', rotation=0, fontsize='large', labelpad= 10)
    colorbar.ax.set_xticklabels(['100% L cochlea', '50%', '0% L==R', '50%', '100% R cochlea'])
    colorbar.ax.invert_xaxis()
    sng_fig.show()


def difference_between_LR_old(allAddr, allTs, p_settings):
    aedat_addr_ts = zip(allAddr, allTs)
    total_time = max(allTs) - min(allTs)
    diff = np.zeros((p_settings.num_channels*2, int(math.ceil(total_time/p_settings.bin_size))))

    spikes = [0 for i in range(p_settings.num_channels*2*2)]
    last_time = aedat_addr_ts[0][1]

    for i in range(int(math.ceil(total_time/p_settings.bin_size))):

        blockAddr = [item[0] for item in aedat_addr_ts if item[1] >= last_time and item[1] < (last_time + p_settings.bin_size)]
        
        for t in range(len(blockAddr)):
            spikes[blockAddr[t]] = spikes[blockAddr[t]] + 1
        
        last_time = last_time + p_settings.bin_size
        diff[:, i] = [x1 - x2 for (x1, x2) in zip(spikes[0:p_settings.num_channels*2], spikes[p_settings.num_channels*2:p_settings.num_channels*2*2])] #  spikes[0:p_settings.num_channels*2] - spikes[p_settings.num_channels*2:p_settings.num_channels*2*2]
        spikes = [0 for i in range(p_settings.num_channels*2*2)]
        
    #print np.max(diff)
    diff = diff*100/max(abs(np.min(diff)), np.max(diff))
    
    # REPRESENTATION
    plt.style.use('default')
    sng_fig = plt.figure()
    sng_fig.canvas.set_window_title('Diff. between L and R cochlea')

    plt.imshow(diff, vmin=-100, vmax=100) #, aspect="auto")
    plt.gca().invert_yaxis()

    plt.xlabel('Bin ('+str(p_settings.bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    plt.title('Diff. between L and R cochlea', fontsize='x-large')

    colorbar = plt.colorbar(ticks=[100, 50, 0, -50, -100], orientation='horizontal')
    colorbar.set_label('Cochlea predominance', rotation=0, fontsize='large', labelpad= 10)
    colorbar.ax.set_xticklabels(['100% L cochlea', '50%', '0% L==R', '50%', '100% R cochlea'])
    colorbar.ax.invert_xaxis()
    sng_fig.show()
