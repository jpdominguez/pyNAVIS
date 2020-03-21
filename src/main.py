import PySimpleGUI as sg
from pyNAVIS_functions.aedat_functions import *
from pyNAVIS_settings.main_settings import *
from pyNAVIS_functions.screens_plot import *
from pyNAVIS_functions.loaders import loadAERDATA


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

sg.ChangeLookAndFeel('SystemDefault')


settings_main_layout =  [[sg.T('This is inside tab 1')]]    

settings_tools_layout = [[sg.T('This is inside tab 2')],    
               [sg.In(key='in')]]    

settings_layout = [[sg.TabGroup([[sg.Tab('Main settings', settings_main_layout, tooltip='tip'), sg.Tab('Tools', settings_tools_layout)]], tooltip='TIP2')],    
          [sg.Button('Save')]]    


menu_def = [['File', ['Load AER-DATA', 'Settings', 'Exit']],      
            ['Plot', ['Spikegram', 'Sonogram', 'Histogram', 'Average activity', 'Disparity between L/R'], ],      
            ['Help', 'About...'], ] 

layout = [[sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Select an .aedat file to load:'), sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False), sg.FileBrowse('Browse AER-DATA', key='browse_AERDATA',  file_types=(("AER-DATA Files", "*.aedat"),))],
          [],
          [sg.Button('Spikegram', key='graph_Spikegram'),
          sg.Button('Histogram', key='graph_Histogram')]]

#form = sg.Window("pyNAVIS", layout)

form = sg.Window("pyNAVIS settings", settings_layout)

while True:
    event, values = form.read()
    if event is None or event == 'Exit':
        break
form.close()

"""
while True:
    event, values = form.read()
    if event is None or event == 'Exit':
        break 
    if event == '_FILEBROWSE_':
        settings = MainSettings(num_channels=num_channels, mono_stereo=mono_stereo, address_size=address_size, ts_tick=ts_tick, bin_size=bin_size, bar_line=bar_line, spikegram_dot_freq=spike_dot_freq, spikegram_dot_size=spike_dot_size)

        spikes_file = loadAERDATA(values['browse_AERDATA'], settings)
        spikes_file = adaptAERDATA(spikes_file, settings)
        checkAERDATA(spikes_file, settings)
        get_info(spikes_file)
    if event == 'graph_Spikegram':
        spikegram(spikes_file, settings, verbose=True)
    if event == 'graph_Histogram':
        histogram(spikes_file, settings, verbose=True)
    if event == 'Settings':
        print('Hey')
    print(event)
"""
form.close()