import random
from pyNAVIS_functions.aedat_functions import save_AERDATA
from pyNAVIS_settings.main_settings import MainSettings

def sweep(freq, cycles, num_ch, length, path):
    addrs = [0] * int(freq*length)
    timestamps = [0] * int(freq*length)


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

    for i in range(freq*length):
        addrs[i] = random.randint(0, num_ch-1)
        timestamps[i] = int(i*1000000/freq) #Multiplying by 1000000 to convert timestamps to microseconds
    
    settings = MainSettings(num_channels = num_ch, mono_stereo = 0)
    save_AERDATA(addrs, timestamps, path, settings)