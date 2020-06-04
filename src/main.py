import os

from examples import gen_random, gen_shift, gen_sweep, load_stereo_AEDAT, manual_split, stereo_to_mono, mono_to_stereo, phaselock
from pyNAVIS import *

dirname = os.path.dirname(__file__)


# Sweep generation example
"""
gen_sweep.run()
"""

# Random addresses generation example
"""
gen_random.run()
"""

# Shift generation example
"""
gen_shift.run()
"""


# Load mono file example 1
"""
settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
load_stereo_AEDAT.run(os.path.join(dirname, 'examples/test_files/130Hz_mono_64ch_ONOFF_addr2b_ts02.aedat'), settings)
"""

# Load mono file example 2
"""
settings = MainSettings(num_channels=32, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
load_stereo_AEDAT.run(os.path.join(dirname, 'examples/test_files/sound_mono_32ch_ONOFF_addr2b_ts02.aedat'), settings)
"""


# Load stereo file example 1
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, ts_tick=1, bin_size=20000)
load_stereo_AEDAT.run(os.path.join(dirname, 'examples/test_files/enun_stereo_64ch_ONOFF_addr4b_ts1.aedat'), settings)
"""

# Load stereo file example 2
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=20000)
load_stereo_AEDAT.run(os.path.join(dirname, 'examples/test_files/523Hz_stereo_64ch_ONOFF_addr2b_ts02.aedat'), settings)
"""

# Manual split example > extracts the first 100ms from the file
"""
settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
manual_split.run(os.path.join(dirname, 'examples/test_files/130Hz_mono_64ch_ONOFF_addr2b_ts02.aedat'), settings)
"""

# Stereo to mono example > extract the left cochlea part of the sound
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, ts_tick=1, bin_size=20000)
stereo_to_mono.run(os.path.join(dirname, 'examples/test_files/enun_stereo_64ch_ONOFF_addr4b_ts1.aedat'), settings, left_right = 0)
"""

# Mono to stereo example > duplicates the mono part and adds a delay of 50ms to the right cochlea part.
"""
settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
mono_to_stereo.run(os.path.join(dirname, 'examples/test_files/130Hz_mono_64ch_ONOFF_addr2b_ts02.aedat'), settings, delay = 50000)
"""

# Phaselock example
"""
settings = MainSettings(num_channels=64, mono_stereo=0, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
phaselock.run(os.path.join(dirname, 'examples/test_files/130Hz_mono_64ch_ONOFF_addr2b_ts02.aedat'), settings)
"""