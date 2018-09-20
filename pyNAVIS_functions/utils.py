import struct
import numpy as np
import matplotlib.pyplot as plt
import math
import time

def extract_addr_and_ts(aedat_addr_ts):
    return [x[0] for x in aedat_addr_ts], [x[1] for x in aedat_addr_ts]

def execution_time(p_function, p_params):
    start_time = time.time()
    p_function(*p_params)
    return time.time() - start_time
