import PySimpleGUI27 as sg
from pyNAVIS_functions.aedat_functions import *
from pyNAVIS_settings.main_settings import MainSettings
from pyNAVIS_functions.screens_plot import *


## PARAMETERS ###############################################################################################################
num_channels = 32      # Number of NAS channels (not addresses but channels).                                               #
mono_stereo = 0        # 0 for a monaural NAS or 1 for a binaural NAS.                                                      #
address_size = 2       # 2 if .aedats are recorded with USBAERmini2 or 4 if .aedats are recorded with jAER.                 #
ts_tick = 0.2          # 0.2 if .aedats are recorded with USBAERmini2 or 1 if .aedats are recorded with jAER.               #
bin_size = 20000       # Time bin (in microseconds) used to integrate the spiking information.                              #
bar_line = 1           # 0 if you want the histogram to be a bar plot or 1 if you want the histogram to be a line plot.     #
spike_dot_freq = 1     # When plotting the cochleogram, it plots one spike for every spike_dot_frPeq spikes.                #
spike_dot_size = 1     # Size of the dots that are plotted on the spikegram                                                 #
#############################################################################################################################

sg.ChangeLookAndFeel('Default1')


settings_layout = [[]]


menu_def = [['File', ['Load AER-DATA', 'Settings', 'Exit']],      
            ['Plot', ['Spikegram', 'Sonogram', 'Histogram', 'Average activity', 'Disparity between L/R'], ],      
            ['Help', 'About...'], ] 

layout = [[sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Select an .aedat file to load:'), sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False), sg.FileBrowse('Browse AER-DATA', key='browse_AERDATA',  file_types=(("AER-DATA Files", "*.aedat"),))],
          [],
          [sg.Button('Spikegram', key='graph_Spikegram')]]

form = sg.Window("pyNAVIS", layout)

while True:
    event, values = form.read()

    if event is None or event == 'Exit':  
        break 
    if event == '_FILEBROWSE_':
        settings = MainSettings(num_channels=num_channels, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)

        add, ts = loadAERDATA(values['browse_AERDATA'], settings)
        ts = adaptAERDATA(ts, settings)
        checkAERDATA(add, ts, settings)
        get_info(add, ts)
    if event == 'graph_Spikegram':  
        #sp = subprocess.Popen([CHROME, values['_URL_']], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        spikegram(add, ts, settings, verbose=True)
    if event == 'Settings':
        print 'Hey'
    print event

form.close()