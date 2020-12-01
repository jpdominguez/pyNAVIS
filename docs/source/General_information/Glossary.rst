Glossary
====================

- **Neuromorphic cochlea**: it a neuromorphic sensors which mimicks the way in which the inner ear works.
- **Neuromorphic Auditory Visualizer**: also called NAS. A digital implementation (FPGA) of a neuromorphic cochlea with a cascade topology designed by Jimenez-Fernandez in 2016.
- **Neuromorphic sensor**: specialized sensory processing functions implemented by either analog or digital electronic circuits that are inspired by biological systems.
- **Action potential**: also called spike. It is the brief reversal of electric polarization of the membrane of a neuron.
- **Channel**: a specific frequency band of the neuromorphic cochlea. Depending on the cochlea, each channel could consists of two spike streams (or addresses), encoding the positive (ON) and the negative (OFF) part of the signal.
- **Address-Event Representation (AER)**: the AER Protocol is an asynchronous handshaking protocol used to transmit signals between neuromorphic systems. Please, refer to *Sivilotti, M. A. (1991). Wiring considerations in analog VLSI systems, with application to field-programmable networks* for more information.
- **MEvents**: megaevents, millions of events, 10^6 events. Commonly used as a unit of measurement for the number of spikes generated.
- **Spikegram**: also called raster plot, cochleagram or cochleogram. A plot where the X axis represents time and the Y axis is the AER address assigned to the spike generated.
- **Sonogram**: plot that represents the spike rate of the cochlea in a color map, where X axis is time, Y axis is the cochlea channel, and the color is the relative spike rate of the channel for a particular time period.
- **Phase-lock**:  Phase-locking is known as matching amplitude times to a certain phase of another waveform. In the case of auditory neurons, this means firing an action potential at a certain phase of a stimulus sound being delivered. It has been seen that when being played a pure tone, auditory nerve fibers will fire at the same frequency as the tone. Volley theory suggests that groups of auditory neurons use phase-locking to represent subharmonic frequencies of one harmonic sound. When phase-locking, ON and OFF spike streams are merged into a single stream, where a spike is generated only when the signal changes from ON to OFF or vice versa. 