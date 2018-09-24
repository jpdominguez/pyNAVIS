from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

def wav_loadWAV(p_path, p_normalize=True):
    samplerate, data = wavfile.read(p_path)

    if p_normalize:
        if data.dtype == 'int16':
            nb_bits = 16 # -> 16-bit wav files
        elif data.dtype == 'int32':
            nb_bits = 32 # -> 32-bit wav files

        data = data / (2.**nb_bits)
    return data, samplerate


def wav_plot(p_data, p_fs):
    times = np.arange(len(p_data))/float(p_fs)

    plt.style.use('seaborn-whitegrid')
    wav_fig = plt.figure()

    wav_fig.canvas.set_window_title('Raw WAV file')
    plt.plot(times, p_data)
    plt.title('Raw WAV file', fontsize='x-large')

    plt.xlabel('Time (ms)', fontsize='large')
    plt.ylabel('Amplitude', fontsize='large')

    wav_fig.show()


def wav_spectrogram(p_data, p_fs):
    plt.style.use('default')
    sptgrm_fig = plt.figure()

    sptgrm_fig.canvas.set_window_title('Spectrogram')
    plt.specgram(p_data,Fs=p_fs)
    plt.title('Spectrogram', fontsize='x-large')

    plt.xlabel('Time (ms)', fontsize='large')
    plt.ylabel('Frequency (Hz)', fontsize='large')
    colorbar = plt.colorbar()
    sptgrm_fig.show()