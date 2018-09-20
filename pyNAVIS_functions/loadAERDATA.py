import struct
import numpy as np
import matplotlib.pyplot as plt
import math

def checkAERDATA(p_timestamps, p_number_of_addresses =  -1, p_events = []):

    # Check all timestamps are greater than zero
    a = all(item >= 0  for item in p_timestamps)

    if not a:
        print "The AER-DATA file that you loaded has at least one timestamp that is below 0."

    # Check every timestamp is greater than its previous one
    b = not any(i > 0 and p_timestamps[i] < p_timestamps[i-1] for i in range(len(p_timestamps)))
    
    if not b:
        print "The AER-DATA file that you loaded has at least one timestamp whose value is lesser than its previous one."

    if p_number_of_addresses != -1:

        # Check all addresses are between zero and the total number of addresses
        c = all(item >= 0 and item < p_number_of_addresses for item in p_events)

        if not c:
            print "The AER-DATA file that you loaded has at least one event whose address is either below 0 or above the number of addresses that you specified."

        return a and b and c

    else:
        return a and not b
            

# Function to subtract the smallest timestamp to all of the events (to start from 0) and adapt them based on the tick frequency of the tool used to log the file.
def adaptAERDATA(p_timestamps, p_timestampReset, p_tick):
    if p_timestampReset:
        return [(x - p_timestamps[0])*p_tick for x in p_timestamps]
    else:
        return [x*p_tick for x in p_timestamps]


def loadAERDATA(p_path, p_address_size = 2):
    events = []
    timestamps = []
    unpack_param = ">H"
    
    if p_address_size == 2:
        unpack_param = ">H"
    elif p_address_size == 4:
        unpack_param = ">L"
    else:
        print "Only address sizes implemented are 2 and 4 bytes"

    with open(p_path, 'rb') as f:
        while True:
            buff = f.read(p_address_size)
            if len(buff) < p_address_size: break
            x = np.uint16(struct.unpack(unpack_param, buff)[0])
            events.append(x)

            buff = f.read(4)
            if len(buff) < 4: break
            x = struct.unpack('>L', buff)[0]
            timestamps.append(x)
    return events, timestamps