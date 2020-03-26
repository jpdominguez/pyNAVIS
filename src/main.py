import os

from examples import gen_random, gen_shift, gen_sweep, load_stereo_AERDATA, manual_split, stereo_to_mono
from pyNAVIS import *

dirname = os.path.dirname(__file__)


#gen_sweep.run()

#gen_random.run()

#gen_shift.run()

"""
settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
load_stereo_AERDATA.run(os.path.join(dirname, 'examples/test_files/stereoPS.aedat'), settings)
"""


"""
settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
manual_split.run(os.path.join(dirname, 'examples/test_files/stereoPS.aedat'), settings)
"""

settings = MainSettings(num_channels=16, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
stereo_to_mono.run(os.path.join(dirname, 'examples/test_files/stereoPS.aedat'), settings, left_right = 0)

