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
import datetime

import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import numpy as np

from .loaders import SpikesFile
from .loaders import LocalizationFile
from .savers import Savers
from .utils import Utils
from .plots import Plots

class Functions:

	@staticmethod
	def check_SpikesFile(spikes_file, settings):
		"""
		Checks if the spiking information contained in the SpikesFile is correct and prints "The loaded SpikesFile file has been checked and it's OK" if the file passes all the checks.
		
		Parameters:
				spikes_file (SpikesFile): File to check.
				settings (MainSettings): Configuration parameters for the file to check.

		Returns:
				None.
		
		Raises:
				TimestampOrderError: If the SpikesFile contains at least one timestamp which value is less than 0.
				TimestampOrderError: If the SpikesFile contains at least one timestamp that is lesser than its previous one.
				AddressValueError: If the SpikesFile contains at least one address less than 0 or greater than the num_channels that you specified in the MainSettings.
		Notes:   
				If mono_stereo is set to 1 (stereo) in the MainSettings, then  addresses should be less than num_channels*2.

				If on_off_both is set to 1 (both) in the MainSettings, then addresses should be less than num_channels*2.
				
				If mono_stereo is set to 1 and on_off_both is set to 1 in the MainSettings, then addresses should be less than num_channels*2*2.
		"""

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
	def check_LocalizationFile(localization_file, settings, localization_settings):
		"""
		Checks if the spiking information contained in the LocalizationFile is correct and prints "The loaded LocalizationFile file has been checked and it's OK" if the file passes all the checks.
		
		Parameters:
				localization_file (LocalizationFile): File to check.
				settings (MainSettings): Configuration parameters for the file to check.
				localization_settings (LocalizationSettings): Configuration parameters of the localization model for the file to check.

		Returns:
				None.
		
		Raises:
				TimestampOrderError: If the LocalizationFile contains at least one timestamp which value is less than 0.
				TimestampOrderError: If the LocalizationFile contains at least one timestamp that is lesser than its previous one.
				ChannelValueError: If the LocalizationFile contains at least one address less than mso_start_channel or greater than mso_end_channel that you specified in the LocalizationSettings.
				NeuronIDValueError: If the LocalizationFile contains at least one address less than 0 or greater than the mso_num_neurons_channel you specified in LocalizationSettings
		Notes:   
				If mso_start_channel is set to 33 and mso_end_channel is set to 36, there will be four possible channel values: [33, 36]
		"""

		# Check if all timestamps are greater than zero
		a = all(item >= 0  for item in localization_file.mso_timestamps)

		if not a:
			print("[Functions.check_LocalizationFile] > TimestampOrderError: The LocalizationFile file that you loaded has at least one timestamp that is less than 0.")

		# Check if each timestamp is greater than its previous one
		b = not any(i > 0 and localization_file.mso_timestamps[i] < localization_file.mso_timestamps[i-1] for i in range(len(localization_file.mso_timestamps)))

		if not b:
			print("[Functions.check_LocalizationFile] > TimestampOrderError: The LocalizationFile file that you loaded has at least one timestamp whose value is lesser than its previous one.")

		# Check if all channel values are between mso_start_channel and mso_end_channel
		c = all(item >= localization_settings.mso_start_channel and item <= localization_settings.mso_end_channel for item in localization_file.mso_channels)

		if not c:
			print("[Functions.check_LocalizationFile] > ChannelValueError: The LocalizationFile file that you loaded has at least one event whose channel value is either less than mso_start_channel or greater than mso_end_channel.")

		# Check if all neuron IDs are between zero and the number of mso_num_neurons_channel
		d = all(item >= 0 and item < localization_settings.mso_num_neurons_channel for item in localization_file.mso_neuron_ids)

		if not d:
			print("[Functions.check_LocalizationFile] > NeuronIDValueError: The LocalizationFile file that you loaded has at least one event whose neuron ID value is either less than zero or greater than mso_num_neurons_channel.")

		if a and b and c and d:
			print("[Functions.check_LocalizationFile] > The loaded LocalizationFile file has been checked and it's OK")

	@staticmethod 
	def adapt_timestamps(timestamps, settings):
		"""
		Subtracts the smallest timestamp of the timestamps list to all of the timestamps contained in the list (in order to start from 0)
		It also adapts timestamps based on the tick frequency (ts_tick in the MainSettings).
		
		Parameters:
				timestamps (int[]): File to adapt.
				settings (MainSettings): Configuration parameters for the file to adapt.

		Returns:
				adapted_timestamps:  Adapted timestamps list.
		"""
		minimum_ts = min(timestamps)
		if settings.reset_timestamp:
			adapted_timestamps = [(x - minimum_ts)*settings.ts_tick for x in timestamps]
		else:
			adapted_timestamps = [x*settings.ts_tick for x in timestamps]
		return adapted_timestamps


	@staticmethod
	def phase_lock(spikes_file, settings, posNeg_both = 0):
		"""
		Performs the phase lock operation over a SpikesFile. This can only be performed to SpikeFiles with both ON and OFF addresses. The phaselock operation puts a spike in the output only when the spike train from a specific channel changes from ON (positive part of the signal) to OFF (negative part of the signal). This heavily reduces the number of spikes at the output.
		
		Parameters:
				spikes_file (SpikesFile): File used to perform the phase lock.
				settings (MainSettings): Configuration parameters of the input file.
				posNeg_both (int, optional): If set to 0, a spike is generated only when spike trains change from ON to OFF addresses. If set to 1, a spike is generated every time spike trains change from ON to OFF addresses or vice versa.

		Returns:
				SpikesFile:  Phase-locked SpikesFile.

		Raises:
				SettingsError: If the on_off_both parameter is not set to 1 (both) in the MainSettings.
		"""

		if settings.on_off_both == 1:
			prevSpike = [None] * (settings.num_channels) * (1 + settings.mono_stereo)
			phaseLockedAddrs = []
			phaseLockedTs = []
			for i in range(len(spikes_file.addresses)):
				if prevSpike[spikes_file.addresses[i]//2] == None:
					prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
				else:
					if (prevSpike[spikes_file.addresses[i]//2] == 0 and spikes_file.addresses[i]%2 == 1) or ((prevSpike[spikes_file.addresses[i]//2] == 1 and spikes_file.addresses[i]%2 == 0) and posNeg_both):
						phaseLockedAddrs.append(spikes_file.addresses[i]//2)
						phaseLockedTs.append(spikes_file.timestamps[i])
						prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
					else:
						prevSpike[spikes_file.addresses[i]//2] = spikes_file.addresses[i]%2
			spikes_file = SpikesFile([], [])
			spikes_file.addresses = phaseLockedAddrs
			spikes_file.timestamps = phaseLockedTs
			return spikes_file
		else:
			print("[Functions.phase_lock] > SettingsError: this functionality cannot be applied to files that do not have ON/positive and OFF/negative addresses. Check the on_off_both setting for more information.")


	@staticmethod
	def stereo_to_mono(spikes_file, left_right, settings, return_save_both = 0, path = None, output_format = '.aedat'):
		"""
		Generates a mono AEDAT SpikesFile from a stereo SpikesFile.

		Parameters:
				spikes_file (SpikesFile): Input file.
				left_right (int): Set to 0 if you want to extract the left part of the SpikesFile, or to 1 if you want the right part.
				settings (MainSettings): Configuration parameters for the input file.
				return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
				path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
				output_format (string, optional): Output format of the file. Currently supports '.aedat', '.csv', ".txt" and ".txt_rel". See the Savers class for more information.
				

		Returns:
				SpikesFile: SpikesFile containing the shift. Returned only if return_save_both is either 0 or 2.
		
		Raises:
				AttributeError: If the input file is a mono SpikesFile (settings.mono_stereo is set to 0).
		"""

		if settings.mono_stereo:
			addr_ts = list(zip(spikes_file.addresses, spikes_file.timestamps))
			addr_ts = [x for x in addr_ts if x[0] >= left_right*settings.num_channels*(settings.on_off_both + 1) and x[0] < (left_right+1)*settings.num_channels*(settings.on_off_both + 1)]

			spikes_file_mono = Utils.extract_addr_and_ts(addr_ts)
			if left_right:
				spikes_file_mono.addresses = [x-left_right*settings.num_channels*(settings.on_off_both + 1) for x in spikes_file_mono.addresses]
			
			
			if return_save_both == 0:
				return spikes_file_mono
			elif return_save_both == 1 or return_save_both == 2:
				Savers.save_as_any(spikes_file_mono, path=path, output_format=output_format, settings=settings) 
				if return_save_both == 2:
					return spikes_file_mono
			
		else:
			print("[Functions.stereo_to_mono] > SettingsError: this functionality cannot be performed over a mono aedat file.")


	@staticmethod
	def mono_to_stereo(spikes_file, delay, settings, return_save_both = 0, path = None, output_format = '.aedat'):
		"""
		Generates a stereo AEDAT SpikesFile from a mono SpikesFile with a specific delay between both.

		Parameters:
				spikes_file (SpikesFile): Input file.
				delay (int): Delay introduced from left and right spikes. Can be either negative or positive.
				settings (MainSettings): Configuration parameters for the input file.
				return_save_both (int, optional): Set it to 0 to return the SpikesFile, to 1 to save the SpikesFile in the output path, and to 2 to do both.
				path (string, optional): Path where the output file will be saved. Format should not be specified. Not needed if return_save_both is set to 0.
				output_format (string, optional): Output format of the file. Currently supports '.aedat', '.csv', ".txt" and ".txt_rel". See the Savers class for more information.

		Returns:
				SpikesFile: SpikesFile containing the shift. Returned only if return_save_both is either 0 or 2.
		
		Raises:
				SettingsError: If the input file is a stereo SpikesFile (settings.mono_stereo is set to 1).
		"""

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
				Savers.save_as_any(spikes_file_new, path=path, output_format=output_format, settings=settings) 
				if return_save_both == 2:
					return spikes_file_new

		else:
			print("[Functions.mono_to_stereo] > SettingsError: this functionality cannot be performed over a stereo aedat file.")        


	@staticmethod
	def extract_channels_activities(spikes_file, addresses, reset_addresses = True, verbose = False):
		"""
		Extract information from a specific set of addresses from the SpikesFile.
		
		Parameters:
				spikes_file (SpikesFile): File to use.
				addresses (int[]): List of addresses to extract.
				reset_addresses (boolean, optional): If set to true, addresses IDs will start from 0. If not, they will keep their original IDs.
				verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

		Returns:
				SpikesFile:  SpikesFile containing only the information from the addresses specified as input from spikes_file.
		"""

		if verbose == True: start_time = time.time()
		spikes_per_channels_ts = []
		spikes_per_channel_addr = []
		for i in range(len(spikes_file.timestamps)):
			if spikes_file.addresses[i] in addresses:
				spikes_per_channels_ts.append(spikes_file.timestamps[i])
				spikes_per_channel_addr.append(spikes_file.addresses[i])
		if verbose == True: print('EXTRACT CHANNELS CALCULATION', time.time() - start_time)
		new_spikes_file = SpikesFile([], [])
		new_spikes_file.addresses = spikes_per_channel_addr
		if reset_addresses == True:
			new_spikes_file.addresses = [addr - addresses[0] for addr in new_spikes_file.addresses]
		new_spikes_file.timestamps = spikes_per_channels_ts
		return new_spikes_file


	@staticmethod
	def PDF_report(spikes_file, settings, output_path, plots = ["Spikegram", "Sonogram", "Histogram", "Average activity", "Difference between L/R"], add_localization_report = False, localization_file = None, localization_settings = None, localization_plots = ["MSO spikegram", "MSO heatmap", "MSO histogram", "MSO localization"], vector = False, verbose = False):
		"""
		Generates a PDF report with the spikegram, sonogram, histogram, average activity and difference between L/R plots obtained from the input SpikesFile or path containing SpikeFiles.
		
		Parameters:
				spikes_file (SpikesFile or string): File or path to use.
				settings (MainSettings): Configuration parameters for the input file.
				output_path (string):
				plots (string list): 
				add_localization_report (boolead, optional):
				localization_settings (LocalizationSettings, optional): 
				localization_plots (string list, optional)
				vector (boolean, optional): Set to True if you want the Spikegram plot vectorized. Note: this may make your PDF heavy.
				verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

		Returns:
				None.
		
		Notes:   
				If the path used as input is a folder instead of a spikes file, the PDF report is generated for every spikes file contained in the folder.
		"""

		if isinstance(spikes_file, str):
    			
			spikes_file_extension = os.path.splitext(spikes_file)

			if spikes_file_extension == ".aedat":
				if add_localization_report == False:
					spikes_file = Loaders.loadAEDAT(spikes_file, settings)
				else:
					spikes_file, localization_file = Loaders.loadAEDATLocalization(spikes_file, settings, localization_settings)
			elif spikes_file_extension == ".csv":
				if add_localization_report == False:
					spikes_file = Loaders.loadCSV(spikes_file, delimiter=',')
				else:
					spikes_file, localization_file = Loaders.loadCSVLocalization(spikes_file, delimiter=',')
			elif spikes_file_extension == ".txt":
				spikes_file, localization_file = Loaders.loadZynqGrabberData(spikes_file, settings, localization_settings)
    				
			spikes_file.timestamps = Functions.adapt_timestamps(spikes_file.timestamps, settings)
			if add_localization_report == True:
				localization_file.timestamps = Functions.adapt_timestamps(localization_file.timestamps, settings)

		if isinstance(spikes_file, SpikesFile):
    		
			pdf = matplotlib.backends.backend_pdf.PdfPages(output_path)
			
			# Spikegram
			if any("Spikegram" in s for s in plots):
				spikegram = Plots.spikegram(spikes_file, settings, )
				pdf.savefig(spikegram)
				plt.draw()
			# Sonogram
			if any("Sonogram" in s for s in plots):
				sonogram = Plots.sonogram(spikes_file, settings)		
				pdf.savefig(sonogram)
				plt.draw()
			# Histogram
			if any("Histogram" in s for s in plots):
				Plots.histogram(spikes_file, settings,)		
				pdf.savefig()
				plt.draw()
			# Average activity
			if any("Average activity" in s for s in plots):
				Plots.average_activity(spikes_file, settings,)		
				pdf.savefig()
				plt.draw()
			# Difference between L/R
			if settings.mono_stereo == 1 and any("Difference between L/R" in s for s in plots):		
				Plots.difference_between_LR(spikes_file, settings,)		
				pdf.savefig()
				plt.draw()

			if add_localization_report == True:
				if isinstance(localization_file, LocalizationFile):
					# MSO spikegram
					if any("MSO spikegram" in s for s in localization_plots):
						mso_spikegram = Plots.mso_spikegram(localization_file, settings, localization_settings)
						pdf.savefig(mso_spikegram)
						plt.draw()
					# MSO heatmap
					if any("MSO heatmap" in s for s in localization_plots):
						mso_heatmap = Plots.mso_heatmap(localization_file, localization_settings)		
						pdf.savefig(mso_heatmap)
						plt.draw()
					# MSO histogram
					if any("MSO histogram" in s for s in localization_plots):
						mso_histogram = Plots.mso_histogram(localization_file, settings, localization_settings)		
						pdf.savefig(mso_histogram)
						plt.draw()
					# MSO localization
					if any("MSO localization" in s for s in localization_plots):
						mso_localization = Plots.mso_localization(localization_file, settings, localization_settings)		
						pdf.savefig(mso_localization)
						plt.draw()
				else:
					print("[Functions.PDF_report] > InputFileError: the input LocalizationFile is not valid.")

			d = pdf.infodict()
			d['Title'] = 'pyNAVIS report'
			d['Author'] = 'Juan P. Dominguez-Morales'
			d['Subject'] = 'pyNAVIS report'
			d['Keywords'] = 'pyNAVIS'
			d['CreationDate'] = datetime.datetime.today()
			d['ModDate'] = datetime.datetime.today()

			pdf.close()

		else:
			print("[Functions.PDF_report] > InputFileError: the input SpikesFile is not valid.")