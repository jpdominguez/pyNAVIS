import random
import numpy as np
from pyNAVIS_settings.main_settings import MainSettings
from pyNAVIS_functions.savers import *

def sweep(freq, cycles, num_ch, length, path, output_format):
    time_per_cycle = float(length) / cycles
    spikes_per_cycle = freq * (num_ch * 2 - 1)
    time_between_spikes = float(time_per_cycle) / spikes_per_cycle

    addrs = [0] * int(spikes_per_cycle*cycles)
    timestamps = [0] * int(spikes_per_cycle*cycles)
    current_spike_id = 0    

    for c in range(cycles):
        for i in range((num_ch*2)-1):
            for j in range(freq):
                addrs[current_spike_id] = i - (i/num_ch)*(((i%(num_ch))+1)*2)
                timestamps[current_spike_id] = int(current_spike_id*time_between_spikes)
                current_spike_id += 1
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)

    if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
        save_AERDATA(addrs, timestamps, path + '.aedat', settings)
    elif output_format == 'csv' or 'CSV' or '.csv':
        save_AERDATA(addrs, timestamps, path + '.aedat', settings)



def shift(freq, num_ch, length, path, output_format):
    total_spikes_no = freq * num_ch
    addrs = [0] * int(total_spikes_no)
    timestamps = [0] * int(total_spikes_no)
    current_spike_id = 0
    
    time_between_spikes = float(length) / total_spikes_no

    for i in range(num_ch):
        for j in range(freq):
            addrs[current_spike_id] = i
            timestamps[current_spike_id] = int(current_spike_id*time_between_spikes)
            current_spike_id += 1
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)



def poisson():
    print "to do"

def random_addrs(freq, num_ch, length, path, output_format):
    addrs = [0] * int(freq*length)
    timestamps = [0] * int(freq*length)
    random.seed('just some random seed')
    for i in range(freq*length):
        addrs[i] = random.randint(0, num_ch-1)
        timestamps[i] = int(i*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds
    
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)