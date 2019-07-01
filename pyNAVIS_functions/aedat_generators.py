import random
import numpy as np
from pyNAVIS_functions.aedat_functions import save_AERDATA
from pyNAVIS_settings.main_settings import MainSettings

def sweep(freq, cycles, num_ch, length, path):
    addrs = [0] * int(freq*length)
    timestamps = [0] * int(freq*length)

    for c in range(cycles):
        for i in range((num_ch-1)*2):
            for j in range((freq*length/num_ch)/cycles - 1):
                #try:
                current_spike_id = j + i*((freq*length/num_ch)/cycles - 1) + c*((num_ch-1)*2)*((freq*length/num_ch)/cycles - 1) #check
                print current_spike_id
                print c, i, j
                addrs[current_spike_id] = (1 - i/num_ch)*i + (i/num_ch)*(num_ch - (i+1)%num_ch)
                timestamps[current_spike_id] = int(current_spike_id*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds  
                #except:
                #    print 'Error', current_spike_id
    print addrs
    print timestamps
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)


def shift(freq, num_ch, length, path):
    addrs = [0] * int(freq*length)
    timestamps = [0] * int(freq*length)

    for i in range(num_ch):
        for j in range(freq*length/num_ch):
            current_spike_id = i * freq*length/num_ch + j
            addrs[current_spike_id] = i
            timestamps[current_spike_id] = int(current_spike_id*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds
    
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)



def poisson():
    #poisson
    a = 1

def random_addrs(freq, num_ch, length, path):
    addrs = [0] * int(freq*length)
    timestamps = [0] * int(freq*length)
    random.seed('just some random seed')
    for i in range(freq*length):
        addrs[i] = random.randint(0, num_ch-1)
        timestamps[i] = int(i*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds
    
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)