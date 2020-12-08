Dataset generators
====================



``pyNAVIS`` incorporates different tools for generating datasets from a set of input files. All of them are included in the :doc:`DatasetGenerators class <../pyNAVIS.dataset_gen>`.

Currently, three dataset generators are implemented:

- **Sonogram dataset generator**: this function receives the path of a folder containing a set of AEDAT files and generates a new folder with their sonograms (in PNG format). This image dataset could be useful for training and testing CNNs or other deep learning algorithms on recognition tasks. This approach was previously used in *Dominguez-Morales, Juan P., et al. "Deep neural networks for the recognition and classification of heart murmurs using neuromorphic auditory sensors." IEEE transactions on biomedical circuits and systems 12.1 (2017): 24-34*.


- **Histogram dataset generator**: this function receives the path of a folder containing a set of AEDAT files and generates a new folder with their histograms in CSV format. This way, each CSV file consits of N rows, where N is the number of channels of the neuromorphic cochlea used to record the original files. These rows represent the number of spikes generated for that specific channel. Therefore, the histogram represents the frequency response of the cochlea for an input file. This could be useful for different scenarios and experiments. As an example, these values could be used as weights for the projections between the first and  the second layer of an SNN in neuromorphic audio recognitions tasks. A similar approach was used in *Dominguez-Morales, Juan Pedro, et al. "Multilayer spiking neural network for audio samples classification using SpiNNaker." International conference on artificial neural networks. Springer, Cham, 2016.*.


- **Phaselock dataset generator**: this function receives the path of a folder containing a set of AEDAT files and generates a new folder with the same files after phase-locking them. When phase-locking, ON and OFF spike streams are merged into a single stream, where a spike is generated only when the signal changes from ON to OFF or vice versa. More information regarding this procedure can be read in the :doc:`Glossary <Glossary>`. The output dataset consists of AEDAT files (one per input file) with less spikes than the original ones, and can be used for further processing, SNN training and many other tasks.