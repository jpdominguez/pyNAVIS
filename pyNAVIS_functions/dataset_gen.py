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

import os
import matplotlib
from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.aedat_functions import *


def generate_sonogram_dataset(path_input_folder, path_output_folder, settings, allow_subdirectories = False, verbose = False):
    if verbose == True:
        print "---- DATASET SONOGRAM GENERATION ----"
        start_time = time.time()    
    if not os.path.exists(path_output_folder):
        os.makedirs(path_output_folder)
    files = []
    progress = 0    
    for r, d, f in os.walk(path_input_folder): # r=root, d=directories, f = files
        for file in f:
            if '.aedat' in file:
                files.append(os.path.join(r, file))
        if allow_subdirectories == False:
            break

    for file in files:
        addrs, ts = loadAERDATA(file, settings)
        sonogram_data = sonogram(addrs, ts, settings, return_data = True)
        matplotlib.image.imsave(os.path.join(path_output_folder, os.path.basename(file)) + '.png', sonogram_data)
        
        if verbose == True:
            progress += 1
            print "Progress: " + str(float(progress)*100/len(files)) + "%"
    
    if verbose == True: print 'Dataset generation process completed. Took ' + str(time.time()-start_time) + " seconds."