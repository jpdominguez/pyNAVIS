import struct
import numpy as np
import matplotlib.pyplot as plt
import math

def extract_addr_and_ts(aedat_addr_ts):
    return [x[0] for x in aedat_addr_ts], [x[1] for x in aedat_addr_ts]