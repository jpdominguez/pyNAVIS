#################################################################################
##                                                                             ##
##    Copyright C 2018  Juan P. Dominguez-Morales                              ##
##                                                                             ##
##    This file is part of pyNAVIS.                                            ##
##                                                                             ##
##    pyNAVIS is free software: you can redistribute it and/or modify          ##
##    it under the terms of the GNU General Public License as published by     ##
##    the Free Software Foundation, either version 3 of the License, or        ##
##    (at your option) any later version.                                      ##
##                                                                             ##
##    pyNAVIS is distributed in the hope that it will be useful,               ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the              ##
##    GNU General Public License for more details.                             ##
##                                                                             ##
##    You should have received a copy of the GNU General Public License        ##
##    along with pyNAVIS.  If not, see <http://www.gnu.org/licenses/>.         ##
##                                                                             ##
#################################################################################

import math
import struct
import time
import copy
import random

import matplotlib.pyplot as plt
import numpy as np

from .loaders import SpikesFile
from .savers import Savers
from .utils import Utils

class Functions:

	@staticmethod
	def check_SpikesFile(spikes_file, settings):
		'''
		Checks if the spiking information contained in the SpikesFile is correct and prints "The loaded SpikesFile file has been checked and it's OK" if the file passes all the checks.
		
		Parameters:
				spikes_file (SpikesFile): file to check.
				settings (MainSettings): configuration parameters for the file to check.

		Returns:
				None.
		
		Raises:
				TimestampOrderError: if the SpikesFile contains at least one timestamp which value is less than 0.
				TimestampOrderError: if the SpikesFile contains at least one timestamp that is lesser than its previous one.
				AddressValueError: if the SpikesFile contains at least one address less than 0 or greater than the num_channels that you specified in the MainSettings.
					NOTE: If mono_stereo is set to 1 (stereo) in the MainSettings, then  addresses should be less than num_channels*2
					NOTE: If on_off_both is set to 1 (both) in the MainSettings, then addresses should be less than num_channels*2.
					NOTE: If mono_stereo is set to 1 and on_off_both is set to 1 in the MainSettings, then addresses should be less than num_channels*2*2.
		'''

		if settings.on_off_both == 1:
			number_of_addresses = settings.num_channels*2
		else:
			number_of_addresses = settings.num_channels
		# Check if all timestamps are greater than zero
		a = all(item >= 0  for item in spikes_file.timestamps)

		if not a:
			print("[Functions.check_SpikesFile] > TimestampOrderError: The SpikesFile file that you loaded has at least one timestamp that is less than 0.")

		# Check if each timestamp is greater than its previous one
		b = not any(i > 0 and spikes_file.timestamps[i] < spikes_file.timestamps[i-1] for i in range(len(spikes_file.timestamps)))

		if not b:
			print("[Functions.check_SpikesFile] > TimestampOrderError: The SpikesFile file that you loaded has at least one timestamp whose value is lesser than its previous one.")

		# Check if all addresses are between zero and the total number of addresses
		c = all(item >= 0 and item < number_of_addresses*(settings.mono_stereo + 1) for item in spikes_file.addresses)

		if not c:
			print("[Functions.check_SpikesFile] > AddressValueError: The SpikesFile file that you loaded has at least one event whose address is either less than 0 or greater than the number of addresses that you specified.")

		if a and b and c:
			print("[Functions.check_SpikesFile] > The loaded SpikesFile file has been checked and it's OK")
				

	@staticmethod 
	def adapt_SpikesFile(spikes_file, settings):
		'''
		Subtracts the smallest timestamp of the SpikesFile to all of the timestamps contained in the file (in order to start from 0)
		It also adapts timestamps based on the tick frequency (ts_tick in the MainSettings).
		
		Parameters:
				spikes_file (SpikesFile): file to adapt.
				settings (MainSettings): configuration parameters for the file to adapt.

		Returns:
				spikes_file (SpikesFile):  adapted SpikesFile.
		'''
		minimum_ts = min(spikes_file.timestamps)
		if settings.reset_timestamp:
			spikes_file.timestamps = [(x - minimum_ts)*settings.ts_tick for x in spikes_file.timestamps]
		else:
			spikes_file.timestamps = [x*settings.ts_tick for x in spikes_file.timestamps]
		return spikes_file


	@staticmethod
	def phase_lock(spikes_file, settings):
		'''
		Performs the phase lock operation over a SpikesFile. This can only be performed to SpikeFiles with both ON and OFF addresses.
		
		Parameters:
				spikes_file (SpikesFile): file used to perform the phase lock.
				settings (MainSettings): configuration parameters of the input file.

		Returns:
				spikes_file (SpikesFile):  phase-locked SpikesFile.

		Raises:
				SettingsError: if the on_off_both parameter is not set to 2 (both) in the MainSettings.
		'''

		if settings.on_off_both == 1:
			prevSpike = [None] * (settings.num_channels) * (1 + settings.mono_stereo)
			phaseLockedAddrs = []
			phaseLockedTs = []
			for i in range(len(spikes_file.addresses)):
				if prevSpike[spikes_file.addresses[i]//2] == None:
					prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
				else:
					if prevSpike[spikes_file.addresses[i]//2] == 0 and spikes_file.addresses[i]%2 == 1:
						phaseLockedAddrs.append(spikes_file.addresses[i]//2)
						phaseLockedTs.append(spikes_file.timestamps[i])
						prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
					else:
						prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
			spikes_file = SpikesFile()
			spikes_file.addresses = phaseLockedAddrs
			spikes_file.timestamps = phaseLockedTs
			return spikes_file
		else:
			print("[Functions.phase_lock] > SettingsError: this functionality cannot be applied to files that do not have ON/positive and OFF/negative addresses. Check the on_off_both setting for more information.")


	@staticmethod
	def stereo_to_mono(spikes_file, left_right, settings, return_save_both = 0, path = None, output_format = '.aedat'):
		'''
		Generates a mono AER-DATA SpikesFile from a stereo SpikesFile.

			Parameters:
					spikes_file (SpikesFile): Input file.
					left_right (int): Set to 0 if you want to extract the left part of the SpikesFile, or to 1 if you want the right part.
					settings (MainSettings): Configuration parameters for the input file.
					return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
					path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                    output_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.
                    

			Returns:
					spikes_file_mono (SpikesFile, optional): SpikesFile containing the shift. Returned only if return_save_both is either 0 or 2.
			
			Raises:
					AttributeError: if the input file is a mono SpikesFile (settings.mono_stereo is set to 0).
		'''

		if settings.mono_stereo:
			addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
			addr_ts = [x for x in addr_ts if x[0] >= left_right*settings.num_channels*(settings.on_off_both + 1) and x[0] < (left_right+1)*settings.num_channels*(settings.on_off_both + 1)]

			spikes_file_mono = Utils.extract_addr_and_ts(addr_ts)
			if left_right:
				spikes_file_mono.addresses = [x-left_right*settings.num_channels*(settings.on_off_both + 1) for x in spikes_file_mono.addresses]
			
			
			if return_save_both == 0:
				return spikes_file_mono
			elif return_save_both == 1 or return_save_both == 2:
				if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
					Savers.save_AERDATA(spikes_file_mono, path + '.aedat', settings)
				elif output_format == 'csv' or 'CSV' or '.csv':
					Savers.save_CSV(spikes_file_mono, path + '.csv', settings)        
				if return_save_both == 2:
					return spikes_file_mono
			
		else:
			print("[Functions.stereo_to_mono] > SettingsError: this functionality cannot be performed over a mono aedat file.")


	@staticmethod
	def mono_to_stereo(spikes_file, delay, settings, return_save_both = 0, path = None, output_format = '.aedat'):
		'''
		Generates a stereo AER-DATA SpikesFile from a mono SpikesFile with a specific delay between both.

			Parameters:
					spikes_file (SpikesFile): Input file.
					delay (int): Delay introduced from left and right spikes. Can be either negative or positive.
					settings (MainSettings): Configuration parameters for the input file.
					return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
					path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
                    output_format (string, optional): Output format of the file. Currently supports '.aedat' and '.csv'.

			Returns:
					spikes_file_new (SpikesFile, optional): SpikesFile containing the shift. Returned only if return_save_both is either 0 or 2.
			
			Raises:
					SettingsError: if the input file is a stereo SpikesFile (settings.mono_stereo is set to 1).
		'''

		if settings.mono_stereo == 0:
			spikes_file_new = copy.deepcopy(spikes_file)
			newAddrs = [(x + settings.num_channels*(settings.on_off_both+1)) for x in spikes_file_new.addresses]
			spikes_file_new.addresses.extend(newAddrs)
			newTs = [(x + delay) for x in spikes_file_new.timestamps]
			spikes_file_new.timestamps.extend(newTs)
			addr_ts = list(zip(spikes_file_new.addresses, spikes_file_new.timestamps))
			addr_ts = sorted(addr_ts, key=lambda v: (v, random.random())) #key=getKey)  #THIS DISORDERS TSS
			spikes_file_new = Utils.extract_addr_and_ts(addr_ts)

			if delay < 0:
				spikes_file_new.timestamps = [x-delay for x in spikes_file_new.timestamps]

			if return_save_both == 0:
				return spikes_file_new
			elif return_save_both == 1 or return_save_both == 2:
				#settings_new = copy.deepcopy(settings)
				#settings_new.mono_stereo = 1
				if output_format == 'aedat' or 'AEDAT' or 'AERDATA' or 'AER-DATA' or 'Aedat' or '.aedat':
					Savers.save_AERDATA(spikes_file_new, path + '.aedat', settings)
				elif output_format == 'csv' or 'CSV' or '.csv':
					Savers.save_CSV(spikes_file_new, path + '.csv', settings)        
				if return_save_both == 2:
					return spikes_file_new

		else:
			print("[Functions.mono_to_stereo] > SettingsError: this functionality cannot be performed over a stereo aedat file.")        



	@staticmethod
	def extract_channels_activities(spikes_file, addresses, verbose = False):
		'''
		Extract information from a specific set of addresses from the SpikesFile.
		
		Parameters:
				spikes_file (SpikesFile): file to use.
				addresses (int[]): list of addresses to extract.
				verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

		Returns:
				new_spikes_file (SpikesFile):  SpikesFile containing only the information from the addresses specified as input from spikes_file.
		'''

		if verbose == True: start_time = time.time()
		spikes_per_channels_ts = []
		spikes_per_channel_addr = []
		for i in range(len(spikes_file.timestamps)):
			if spikes_file.addresses[i] in addresses:
				spikes_per_channels_ts.append(spikes_file.timestamps[i])
				spikes_per_channel_addr.append(spikes_file.addresses[i])
		if verbose == True: print('EXTRACT CHANNELS CALCULATION', time.time() - start_time)
		new_spikes_file = SpikesFile()
		new_spikes_file.addresses = spikes_per_channel_addr
		new_spikes_file.timestamps = spikes_per_channels_ts
		return new_spikes_file