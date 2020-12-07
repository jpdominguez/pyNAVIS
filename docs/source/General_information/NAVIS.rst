.. |check| raw:: html

    <input checked=""  type="checkbox">

.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">


********************
NAVIS and pyNAVIS
********************

``pyNAVIS`` stands for python-based Neuromorphic Auditory Visualizer (NAVIS). NAVIS is a GUI-based software tool for neuromorphic researchers to analyze spiking information obtained from a neuromorphic cochlea.

`NAVIS was also developed by us <https://github.com/jpdominguez/NAVIS-Tool>`_, and it is the foundation of what pyNAVIS currently is. `It was published in Neurocomputing journal <https://www.sciencedirect.com/science/article/pii/S0925231216315624>`_  as an Original Software Publication. 

It was built on Windows Presentation Foundation (WPF), which allows an interactive GUI for fast analysis of a recorded file from a neuromorphic cochlea. As a counterpart, NAVIS is only available for Windows OS users due to its \ac{GUI} framework dependency.

For this purpose, and based on many requests from different users and research groups with which the authors have collaborated, we developed pyNAVIS, a python version of that tool with many other functionalities added.

If you move from NAVIS to pyNAVIS, you will find the same whole set of functionalities. Moreover, some new useful functionalities suggested by neuromorpihc researchers in different research interships, international conferences and workshops (CapoCaccia Neuromorphic Workshop and Telluride Neuromorphic Cognition Engineering Workshop) that we've been to have already been implemented.

``pyNAVIS`` does not have any GUI, which makes it lighter and faster. It is also very useful not only for being used as a standalone software package, but also to be imported within a bigger project and benefit from its functionalities. Due to the lack of an user interface, adding new functionalities to it is easier and faster than in NAVIS.

The following table summarizes the comparison between the main functionalities that NAVIS and pyNAVIS have:


+------------------------------------------------------+------------+----------+
|                     Functionality                    |    NAVIS   |  pyNAVIS |
+=======================+==============================+============+==========+
| Loaders               | \- Load AEDAT                |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Load CSV                  |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Load ZynqGrabber (iCub)   | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+
| Plots                 | \- Spikegram                 |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Sonogram                  |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Histogram                 |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Average activity          |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Difference between L/R    |  |check_|  | |check_| |
+-----------------------+------------------------------+------------+----------+
| Savers                | \- Save to AEDAT             |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Save to CSV               |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Save to TXT               | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+
| Splitters             | \- Manual Splitter           |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Automatic Splitter        |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Segmenter                 | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+
| Generators            | \- Random addresses          | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Shift                     | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Sweep                     | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+
| Dataset generation    | \- Phaselock dataset         | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Sonogram dataset          | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Histogram dataset         | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+
| Other functionalities | \- Mono to stereo            |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Stereo to mono            |  |check_|  | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Phaselock                 | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Extract channels activity | |uncheck_| | |check_| |
|                       +------------------------------+------------+----------+
|                       | \- Check input file          | |uncheck_| | |check_| |
+-----------------------+------------------------------+------------+----------+

Apart from that, it is also important to mention a few aspects:

- pyNAVIS is cross platform, while NAVIS only works in Windows.
- pyNAVIS can be easily integrated with other tools. Just by importing the pyNAVIS library in your script you can start using any of its functionalities. NAVIS cannot be integrated with other projects unless you dig deep in the code and merge it with another WPF application.
- pyNAVIS does not have a GUI, while NAVIS does.
- It is way easier to implement new functionalities in pyNAVIS than in NAVIS. Developers only need the basics of Python for that. In NAVIS, developers would need expertise on C#, LINQ and WPF and integrate the new function in the GUI.
- Although we will continue updating NAVIS and adding new functionalities to it, users are moving towards using pyNAVIS as the reference software for neuromorphic audio processing and analysis.