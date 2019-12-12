import struct
import math

class SpikesFile:
    timestamps = []
    addresses = []


def loadAERDATA(path, settings):
    unpack_param = ">H"
    
    if settings.address_size == 2:
        unpack_param = ">H"
    elif settings.address_size == 4:
        unpack_param = ">L"
    else:
        print("Only address sizes implemented are 2 and 4 bytes")

    with open(path, 'rb') as f:
        ## Check header ##
        p = 0
        lt = f.readline()
        while lt and lt[0] == "#":
            p += len(lt)
            lt = f.readline()
        f.seek(p)

        f.seek(0, 2)
        eof = f.tell()

        num_events = math.floor((eof-p)/(settings.address_size + 4))

        f.seek(p)

        events = [0] * int(num_events)
        timestamps = [0] * int(num_events)

        ## Read file ##
        i = 0
        try:
            while 1:
                buff = f.read(settings.address_size)
                x = struct.unpack(unpack_param, buff)[0]
                events[i] = x

                buff = f.read(4)
                x = struct.unpack('>L', buff)[0]
                timestamps[i] = x

                i += 1
        except Exception as inst:
            pass
    spikes_file = SpikesFile()
    spikes_file.addresses = events
    spikes_file.timestamps = timestamps
    return spikes_file