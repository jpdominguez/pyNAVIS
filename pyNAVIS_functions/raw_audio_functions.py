#################################################################################
##                                                                             ##
##    Copyright © 2018  Juan P. Dominguez-Morales                              ##
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

from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

def wav_loadWAV(path, normalize=True):
    samplerate, data = wavfile.read(path)

    if normalize:
        if data.dtype == 'int16':
            nb_bits = 16 # -> 16-bit wav files
        elif data.dtype == 'int32':
            nb_bits = 32 # -> 32-bit wav files

        data = data / (2.**nb_bits)
    return data, samplerate


def wav_plot(data, fs):
    times = np.arange(len(data))/float(fs)

    plt.style.use('seaborn-whitegrid')
    wav_fig = plt.figure()

    wav_fig.canvas.set_window_title('Raw WAV file')
    plt.plot(times, data)
    plt.title('Raw WAV file', fontsize='x-large')

    plt.xlabel('Time (ms)', fontsize='large')
    plt.ylabel('Amplitude', fontsize='large')

    wav_fig.show()


def wav_spectrogram(data, fs):
    plt.style.use('default')
    sptgrm_fig = plt.figure()

    sptgrm_fig.canvas.set_window_title('Spectrogram')
    plt.specgram(data,Fs=fs)
    plt.title('Spectrogram', fontsize='x-large')

    plt.xlabel('Time (ms)', fontsize='large')
    plt.ylabel('Frequency (Hz)', fontsize='large')
    colorbar = plt.colorbar()
    sptgrm_fig.show()