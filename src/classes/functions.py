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

import matplotlib.pyplot as plt
import numpy as np

from .loaders import SpikesFile

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
				ValueError: if the SpikesFile contains at least one timestamp which value is less than 0.
				ValueError: if the SpikesFile contains at least one timestamp that is lesser than its previous one.
				ValueError: if the SpikesFile contains at least one address less than 0 or greater than the num_channels that you specified in the MainSettings.
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
			raise ValueError("The SpikesFile file that you loaded has at least one timestamp that is less than 0.")

		# Check if each timestamp is greater than its previous one
		b = not any(i > 0 and spikes_file.timestamps[i] < spikes_file.timestamps[i-1] for i in range(len(spikes_file.timestamps)))

		if not b:
			raise ValueError("The SpikesFile file that you loaded has at least one timestamp whose value is lesser than its previous one.")

		# Check if all addresses are between zero and the total number of addresses
		c = all(item >= 0 and item < number_of_addresses*(settings.mono_stereo+1) for item in spikes_file.addresses)

		if not c:
			raise ValueError("The SpikesFile file that you loaded has at least one event whose address is either less than 0 or greater than the number of addresses that you specified.")

		if a and b and c:
			print("The loaded SpikesFile file has been checked and it's OK")
				

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
				AttributeError: if the on_off_both parameter is not set to 2 (both) in the MainSettings.
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
			raise AttributeError("Phase Lock: this functionality cannot be applied to files that do not have ON/positive and OFF/negative addresses. Check the on_off_both setting for more information.")


	@staticmethod
	def stereoToMono(spikes_file, left_right, path, settings): # NEEDS TO BE TESTED
		'''
		Generates a mono AER-DATA SpikesFile from a stereo SpikesFile.

			Parameters:
					spikes_file (SpikesFile): Input file.
					left_right (int): Set to 0 if you want to extract the left part of the SpikesFile, or to 1 if you want the right part.
					path (string, optional): Path where the output file will be saved. Filename and format should be specified.
					settings (MainSettings): Configuration parameters for the input file.

			Returns:
					None.
			
			Raises:
				AttributeError: if the input file is a mono SpikesFile (settings.mono_stereo is set to 0).
		'''

		if settings.mono_stereo:
			aedat_addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
			aedat_addr_ts = [x for x in aedat_addr_ts if x[0] >= left_right*settings.num_channels*2 and x[0] < (left_right+1)*settings.num_channels*2]

			spikes_file_mono = extract_addr_and_ts(aedat_addr_ts)
			if left_right:
				spikes_file_mono.addresses = [x-left_right*settings.num_channels*2 for x in spikes_file_mono.addresses]
			save_AERDATA(spikes_file, path, settings)
		else:
			raise AttributeError("StereoToMono: this functionality cannot be performed over a mono aedat file.")


	@staticmethod
	def monoToStereo(spikes_file, delay, path, settings):
		'''
		Generates a stereo AER-DATA SpikesFile from a mono SpikesFile with a specific delay between both.

			Parameters:
					spikes_file (SpikesFile): Input file.
					delay (int): Delay introduced from left and right spikes. Can be either negative or positive.
					path (string, optional): Path where the output file will be saved. Filename and format should be specified.
					settings (MainSettings): Configuration parameters for the input file.

			Returns:
					None.
			
			Raises:
				AttributeError: if the input file is a stereo SpikesFile (settings.mono_stereo is set to 1).
		'''

		if settings.mono_stereo == 0:
			spikes_file_new = copy.deepcopy(spikes_file)
			newAddrs = [(x + settings.num_channels*(settings.on_off_both+1)) for x in spikes_file_new.addresses]
			spikes_file_new.addresses.extend(newAddrs)
			newTs = [(x + delay) for x in spikes_file_new.timestamps]
			spikes_file_new.timestamps.extend(newTs)
			aedat_addr_ts = list(zip(spikes_file_new.addresses, spikes_file_new.timestamps))
			aedat_addr_ts = sorted(aedat_addr_ts, key=lambda v: (v, random.random())) #key=getKey)  #THIS DISORDERS TSS
			spikes_file_new = extract_addr_and_ts(aedat_addr_ts)

			settings_new = copy.deepcopy(settings)
			settings_new.mono_stereo = 1
			save_AERDATA(spikes_file_new, path, settings_new)
		else:
			raise AttributeError("MonoToStereo: this functionality cannot be performed over a stereo aedat file.")        



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


	@staticmethod
	def get_info(spikes_file):
		'''
		Prints the number of spikes and the number of microseconds of audio that the SpikesFile contains.
		
		Parameters:
				spikes_file (SpikesFile): file to get the information from.

		Returns:
				None.
		'''

		print("The file contains", len(spikes_file.addresses), "spikes")
		print("The audio has", max(spikes_file.timestamps), 'microsec')