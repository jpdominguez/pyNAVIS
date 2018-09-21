import math
import struct

import matplotlib.pyplot as plt
import numpy as np

def sonogram(allAddr, allTs, num_channels, bin_size):

    aedat_addr_ts = zip(allAddr, allTs)
    total_time = max(allTs) - min(allTs)
    sonogram = np.zeros((num_channels*2, int(math.ceil(total_time/bin_size))))

    spikes = [0 for i in range(num_channels*2)]
    last_time = aedat_addr_ts[0][1]

    for i in range(int(math.ceil(total_time/bin_size))):

        blockAddr = [item[0] for item in aedat_addr_ts if item[1] >= last_time and item[1] < (last_time + bin_size)]

        for t in range(len(blockAddr)):
            spikes[blockAddr[t]] = spikes[blockAddr[t]] + 1
    
        last_time = last_time + bin_size
        sonogram[:, i] = spikes
        spikes = [0 for i in range(num_channels*2)]

    
    # REPRESENTATION
    plt.style.use('default')
    sng_fig = plt.figure()
    sng_fig.canvas.set_window_title('Sonogram')

    plt.imshow(sonogram) #, aspect="auto")
    plt.gca().invert_yaxis()

    plt.xlabel('Bin ('+str(bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    plt.title('Sonogram', fontsize='x-large')

    colorbar = plt.colorbar()
    colorbar.set_label('No. of spikes', rotation=270, fontsize='large', labelpad= 10) #, rotation=270)

    sng_fig.show()


def spikegram(allAddr, allTs, p_settings):

    #REPRESENTATION
    plt.style.use('seaborn-whitegrid')
    spk_fig = plt.figure()
    spk_fig.canvas.set_window_title('Spikegram')

    if p_settings.mono_stereo == 0:
        plt.scatter(allTs, allAddr, s=p_settings.spikegram_dot_size)
    else:
        """
        col = np.where([x for x in allAddr if x <p_settings.num_channels*(p_settings.on_off_both)],'y','k')
        print col
        plt.scatter(allTs, allAddr, s=p_settings.spikegram_dot_size, c=col)
        """
        aedat_addr_ts = zip(allAddr, allTs)
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] < p_settings.num_channels*(p_settings.on_off_both)])
        plt.scatter(ts, addr, s=p_settings.spikegram_dot_size, c='#80bdf7')
        addr, ts = zip(*[(evt[0], evt[1]) for evt in aedat_addr_ts if evt[0] >= p_settings.num_channels*(p_settings.on_off_both) and evt[0] < p_settings.num_channels*(p_settings.on_off_both)*2])
        plt.scatter(ts, addr, s=p_settings.spikegram_dot_size, c='#fcbd6a')
        



    plt.title('Spikegram', fontsize='x-large')

    plt.xlabel('Timestamp ($\mu$s)', fontsize='large')
    plt.ylabel('Address', fontsize='large')

    spk_fig.show()



def histogram(allAddr, num_channels, mono_stereo, bar_line):

    spikes_count = np.zeros(num_channels * 2 * (mono_stereo + 1))

    for event in allAddr:
        spikes_count[event] = spikes_count[event] + 1

    plt.style.use('seaborn-whitegrid')
    hst_fig = plt.figure()
    hst_fig.canvas.set_window_title('Histogram')
    plt.title('Histogram', fontsize='x-large')
    plt.xlabel('Address', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    if bar_line == 0:
        plt.bar(np.arange(num_channels * 2 * (mono_stereo + 1)), spikes_count)
    else:
        plt.plot(np.arange(num_channels * 2 * (mono_stereo + 1)), spikes_count)

    hst_fig.show()


def average_activity(allTs, bin_size):
    total_time = int(max(allTs))
    last_ts = 0
    average_activity = np.zeros(int(math.ceil(total_time/bin_size))+1)
    for i in range(0, total_time, bin_size):
        spikes_between_timestamps = [ts for ts in allTs if ts >= last_ts and ts < last_ts + bin_size]
        average_activity[int(i/bin_size)] = len(spikes_between_timestamps)
        last_ts = last_ts + bin_size

    plt.style.use('seaborn-whitegrid')
    avg_fig = plt.figure()
    avg_fig.canvas.set_window_title('Average activity')
    plt.title('Average activity', fontsize='x-large')
    plt.xlabel('Bin ('+str(bin_size) + '$\mu$s width)', fontsize='large')
    plt.ylabel('No. of spikes', fontsize='large')

    plt.plot(np.arange(math.ceil(total_time/bin_size)+1), average_activity)
    avg_fig.show()
