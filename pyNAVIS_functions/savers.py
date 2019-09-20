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

def save_AERDATA(blockAddr, blockTs, path, settings, verbose = 0):
    start_time = time.time()
    unpack_param = '>L'
    if settings.address_size == 2:
        unpack_param = ">H"
    elif settings.address_size == 4:
        unpack_param = ">L"

    with open(path, 'wb') as f:
        for i in range(len(blockAddr)):
            addr = struct.pack(unpack_param, blockAddr[i])
            ts = struct.pack('>L', blockTs[i]/settings.ts_tick)
            f.write(addr)
            f.write(ts)
        if verbose == 1:
            print "AERDATA file saved correctly.Took:", time.time() - start_time, 'seconds'


def save_CSV(blockAddr, blockTs, path, verbose = 0):
    if verbose == 1: 
        start_time = time.time()

    with open(path + '.csv', 'wb') as f:
        for i in range(len(blockAddr)):
            f.write(str(blockAddr[i]) + ', ' + str(blockTs[i]) + "\n")    
    if verbose == 1:
        print "TXT fie saved correctly. Took:", time.time() - start_time, "seconds"


def save_TXT(blockAddr, blockTs, path, verbose = 0):
    if verbose == 1: 
        start_time = time.time()

    with open(path+'_addrs.txt', 'wb') as f:
        for addr in blockAddr:
            f.write(str(addr) + '\n')
    with open(path+'_tss.txt', 'wb') as f:
        for ts in blockTs:
            f.write(str(ts) + '\n')    
    if verbose == 1:
        print "TXT fie saved correctly. Took:", time.time() - start_time, "seconds"