import os

from examples import gen_random, gen_shift, gen_sweep, load_stereo_AEDAT, manual_split, stereo_to_mono, mono_to_stereo, phaselock, load_stereo_localization_AEDAT, load_stereo_localization_CSV, load_stereo_localization_ZynqGrabber
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

# Loading .aedat with localization information (jAER)
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, ts_tick=1, bin_size=20000)
settings_localization = LocalizationSettings(mso_start_channel=33, mso_end_channel=36, mso_num_neurons_channel=32)
load_stereo_localization_AEDAT.run(os.path.join(dirname, 'examples/test_files/500Hz_stereo_64ch_ONOFF_addr4b_ts1_mso_33_36_nid_16_loc_center.aedat'), settings, settings_localization)
"""

# Loading .aedat with localization information (MATLAB)
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=2, ts_tick=0.2, bin_size=10000)
settings_localization = LocalizationSettings(mso_start_channel=33, mso_end_channel=36, mso_num_neurons_channel=31)
load_stereo_localization_AEDAT.run(os.path.join(dirname, 'examples/test_files/chirp_200_2000Hz_stereo_64ch_ONOFF_addr4b_ts1_mso_25_35_nid_16_loc_left.aedat'), settings, settings_localization)
"""

# Loading CSV from simulation with only localization information (SOC simulation)
"""
settings = MainSettings(num_channels=64, mono_stereo=1, on_off_both=1, address_size=4, ts_tick=1, bin_size=20000)
settings_localization = LocalizationSettings(mso_start_channel=33, mso_end_channel=36, mso_num_neurons_channel=16)
load_stereo_localization_CSV.run(os.path.join(dirname, 'examples/test_files/pure_tone_fs48000duration1000frequency500amplitude1_3_soc_out3.txt'), settings, settings_localization, include_nas=False)
"""

# Loading CSV from ZynqGrabber output (iCub) and generate a PDF report
# NOTE: for files recorded using iCub, both the MainSettings and LocalizationSettings are fixed.
"""
settings = MainSettings(num_channels=32, mono_stereo=1, on_off_both=1, ts_tick=80e-3, bin_size=100000)
settings_localization = LocalizationSettings(mso_start_channel=13, mso_end_channel=16, mso_num_neurons_channel=16)
load_stereo_localization_ZynqGrabber.run(os.path.join(dirname, 'examples/test_files/500Hz_head_sweep_stereo_32ch_ONOFF_zynq_decoded_events.txt'), settings, settings_localization)
"""