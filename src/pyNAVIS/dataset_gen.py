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

from .functions import Functions
from .loaders import Loaders
from .plots import Plots
from .savers import Savers

class DatasetGenerators:

    @staticmethod
    def generate_sonogram_dataset(path_input_folder, path_output_folder, settings, allow_subdirectories = False, verbose = False):
        """
        Automatically generates and saves sonograms from a set of AER-DATA files.
        
        Parameters:
                path_input_folder (string): Path of the folder where AER-DATA files are.
                path_output_folder (string): Path of the folder where sonogram images will be saved.
                settings (MainSettings): Configuration parameters of the files in the path_input_folder.
                allow_subdirectories (boolean, optional): Allow the function to navigate deeper in the path_input_folder folder structure to look for input files.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        if verbose == True:
            print("---- SONOGRAM DATASET GENERATION ----")
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
            spikes_file = Loaders.loadAERDATA(file, settings)
            sonogram_data = Plots.sonogram(spikes_file.addresses, spikes_file.timestamps, settings, return_data = True)
            matplotlib.image.imsave(os.path.join(path_output_folder, os.path.basename(file)) + '.png', sonogram_data)
            
            if verbose == True:
                progress += 1
                print("Progress: " + str(float(progress)*100/len(files)) + "%")
        
        if verbose == True: print('Dataset generation process completed. Took ' + str(time.time()-start_time) + " seconds.")


    def generate_phaselock_dataset(path_input_folder, path_output_folder, settings, allow_subdirectories = False, verbose = False):
        """
        Automatically generates and saves phaselocked AER-DATA files from a set of AER-DATA files.
        
        Parameters:
                path_input_folder (string): Path of the folder where AER-DATA files are.
                path_output_folder (string): Path of the folder where phaselocked AER-DATA files will be saved.
                settings (MainSettings): Configuration parameters of the files in the path_input_folder.
                allow_subdirectories (boolean, optional): Allow the function to navigate deeper in the path_input_folder folder structure to look for input files.
                verbose (boolean, optional): Set to True if you want the execution time of the function to be printed.

        Returns:
                None.
        """

        if verbose == True:
            print("---- PHASELOCK DATASET GENERATION ----")
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
            spikes_file = Loaders.loadAERDATA(file, settings)
            #sonogram_data = Plots.sonogram(spikes_file.addresses, spikes_file.timestamps, settings, return_data = True)
            #matplotlib.image.imsave(os.path.join(path_output_folder, os.path.basename(file)) + '.png', sonogram_data)
            phaselocked_spikes = Functions.phase_lock(spikes_file, settings)
            Savers.save_AERDATA(phaselocked_spikes, os.path.join(path_output_folder, os.path.basename(file)), settings)
            
            if verbose == True:
                progress += 1
                print("Progress: " + str(float(progress)*100/len(files)) + "%")
        
        if verbose == True: print('Dataset generation process completed. Took ' + str(time.time()-start_time) + " seconds.")