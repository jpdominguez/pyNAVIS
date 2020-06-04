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

class Utils:

	@staticmethod
	def extract_addr_and_ts(zipped_addr_ts):
		"""
		Converts a list of [address, timestamp] tuples into a SpikesFile.

		Parameters:
				aedat_addr_ts (list): A list of [address, timestamp] tuples.

		Returns:
				SpikesFile: A SpikesFile object with the addresses and timestamps obtained from zipped_addr_ts
		"""

		spikes_file = SpikesFile([], [])
		spikes_file.addresses = [x[0] for x in zipped_addr_ts]
		spikes_file.timestamps = [x[1] for x in zipped_addr_ts]
		return spikes_file

	@staticmethod
	def execution_time(executing_function, function_params):
		"""
		Calculate the time that a function takes to execute (in seconds).

		Parameters:
				executing_function (function): The name of the function whose execution time wants to be calculated.
				function_params (list): List of the parameters that want to be used in the executing_function.

		Returns:
				float: Time that the function takes to execute.
		"""

		start_time = time.time()
		executing_function(*function_params)
		total_time = time.time() - start_time
		return total_time

	
	@staticmethod
	def getKey(item):
		"""
		Get timestamps. Used to sort zipped list of [address, timestamp] tuples by timestamp.

		Parameters:
				item (tuple): [address, timestamp] tuple.

		Returns:
				int: Timestamp.
		"""

		return item[1]

	@staticmethod
	def order_timestamps(spikes_file):
		"""
		Order the spikes contained in a SpikesFile by timestamp.

		Parameters:
				spikes_file (SpikesFile): Input SpikesFile to order.

		Returns:
				SpikesFile: Ordered SpikesFile.
		"""
	
		aedat_addr_ts = zip(spikes_file.addresses, spikes_file.timestamps)
		aedat_addr_ts = sorted(aedat_addr_ts, key=Utils.getKey)
		spikes_file_ordered = Utils.extract_addr_and_ts(aedat_addr_ts)
		return spikes_file_ordered

	@staticmethod
	def get_info(spikes_file):
		"""
		Prints the number of spikes and the number of microseconds of audio that the SpikesFile contains.
		
		Parameters:
				spikes_file (SpikesFile): File to get the information from.

		Returns:
				None.
		"""

		print("The file contains", len(spikes_file.addresses), "spikes")
		print("The audio has", max(spikes_file.timestamps), 'microsec')