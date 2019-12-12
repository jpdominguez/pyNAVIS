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

import struct
import time

def save_AERDATA(spikes_file, path, settings, verbose = False):
    if verbose == True: start_time = time.time()
    unpack_param = '>L'
    if settings.address_size == 2:
        unpack_param = ">H"
    elif settings.address_size == 4:
        unpack_param = ">L"

    with open(path, 'wb') as f:
        for i in range(len(spikes_file.addresses)):
            addr = struct.pack(unpack_param, int(spikes_file.addresses[i]))
            ts = struct.pack('>L', int(spikes_file.timestamps[i]//settings.ts_tick))
            f.write(addr)
            f.write(ts)
        if verbose == True:
            print("AERDATA file saved correctly.Took:", time.time() - start_time, 'seconds')


def save_CSV(spikes_file, path, verbose = False):
    if verbose == True: start_time = time.time()

    with open(path + '.csv', 'w') as f:
        for i in range(len(spikes_file.addresses)):
            f.write(str(spikes_file.addresses[i]) + ', ' + str(int(spikes_file.timestamps[i])) + "\n")    
    if verbose == True:
        print("CSV fie saved correctly. Took:", time.time() - start_time, "seconds")


def save_TXT(spikes_file, path, verbose = False):
    if verbose == True: start_time = time.time()

    with open(path+'_addrs.txt', 'w') as f:
        for addr in spikes_file.addresses:
            f.write(str(addr) + '\n')
    with open(path+'_tss.txt', 'w') as f:
        for ts in spikes_file.timestamps:
            f.write(str(int(ts)) + '\n')    
    if verbose == True:
        print("TXT fie saved correctly. Took:", time.time() - start_time, "seconds")


def save_TXT_relativeTS(spikes_file, path, verbose = False):
    if verbose == True: start_time = time.time()

    with open(path+'_addrs.txt', 'w') as f:
        for addr in spikes_file.addresses:
            f.write(str(addr) + '\n')
    with open(path+'_tss.txt', 'w') as f:
        for i in range(len(spikes_file.timestamps)):
            if i == 0:
                f.write(str(0) + '\n')
            else:
                f.write(str(int(spikes_file.timestamps[i]-spikes_file.timestamps[i-1])) + '\n')    
    if verbose == True:
        print("TXT fie saved correctly. Took:", time.time() - start_time, "seconds")