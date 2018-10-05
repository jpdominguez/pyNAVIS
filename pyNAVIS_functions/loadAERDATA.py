import struct
import numpy as np
import matplotlib.pyplot as plt
import math

def checkAERDATA(p_events, p_timestamps, p_settings):

    number_of_addresses = p_settings.num_channels*2
    # Check all timestamps are greater than zero
    a = all(item >= 0  for item in p_timestamps)

    if not a:
        print "The AER-DATA file that you loaded has at least one timestamp that is below 0."

    # Check every timestamp is greater than its previous one
    b = not any(i > 0 and p_timestamps[i] < p_timestamps[i-1] for i in range(len(p_timestamps)))

    if not b:
        print "The AER-DATA file that you loaded has at least one timestamp whose value is lesser than its previous one."

    # Check all addresses are between zero and the total number of addresses
    c = all(item >= 0 and item < number_of_addresses*(p_settings.mono_stereo+1) for item in p_events)

    if not c:
        print "The AER-DATA file that you loaded has at least one event whose address is either below 0 or above the number of addresses that you specified."

    if a and b and c:
        print "The loaded AER-DATA file has been checked and it's OK"
            

# Function to subtract the smallest timestamp to all of the events (to start from 0) and adapt them based on the tick frequency of the tool used to log the file.
def adaptAERDATA(p_timestamps, p_settings):
    minimum_ts = min(p_timestamps)
    if p_settings.reset_timestamp:
        return [(x - minimum_ts)*p_settings.ts_tick for x in p_timestamps]
    else:
        return [x*p_settings.ts_tick for x in p_timestamps]


def loadAERDATA(p_path, p_settings):
    unpack_param = ">H"
    
    if p_settings.address_size == 2:
        unpack_param = ">H"
    elif p_settings.address_size == 4:
        unpack_param = ">L"
    else:
        print "Only address sizes implemented are 2 and 4 bytes"

    with open(p_path, 'rb') as f:
        ## Check header ##
        p = 0
        lt = f.readline()
        while lt and lt[0] == "#":
            p += len(lt)
            lt = f.readline()
        f.seek(p)

        f.seek(0, 2)
        eof = f.tell()

        num_events = math.floor((eof-p)/(p_settings.address_size + 4))

        f.seek(p)

        events = [0] * int(num_events)
        timestamps = [0] * int(num_events)

        ## Read file ##
        i = 0
        try:
            while 1:
                buff = f.read(p_settings.address_size)                
                x = struct.unpack(unpack_param, buff)[0]
                events[i] = x

                buff = f.read(4)
                x = struct.unpack('>L', buff)[0]
                timestamps[i] = x

                i += 1
        except Exception as inst:
            pass
    return events, timestamps