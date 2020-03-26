
**************************
pyNAVIS: a cross-platform Neuromorphic Auditory VISualizer
**************************

.. image:: https://img.shields.io/pypi/v/pyNAVIS.svg
   :target: https://pypi.python.org/pypi/pyNAVIS
   :alt: Pypi Version 
.. image:: https://img.shields.io/pypi/l/pyNAVIS.svg
   :target: https://pypi.python.org/pypi/pyNAVIS/
   :alt: License
.. image:: https://readthedocs.org/projects/pyNAVIS/badge/
  :target: http://pyNAVIS.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

``pyNAVIS`` is an open-source cross-platform Python module for analyzing and processing spiking information obtained from neuromorphic auditory sensors. It is primarily focused to be used with a NAS_, but can work with any other cochlea sensor.

For more information, head over to the `Github repository <https://github.com/jpdominguez/pyNAVIS>`_.

.. _NAS: https://github.com/RTC-research-group/OpenNAS

Installing
==========

``pyNAVIS`` is distributed on PyPI_ and can be installed with pip::

   pip install pyNAVIS

For more information, head over to the :doc:`Installing section <Installing>`.

.. _PyPI: https://pypi.python.org/pypi/pyNAVIS


Getting started
===============

Now that you have everything set up, you can create a new Python file and import the package:

.. prompt:: python \

   from pyNAVIS import *

With this, you can now use all the functionalities that ``pyNAVIS`` provides. A more detailed guide with examples can be read :doc:`here <Getting started>`.


Software package
================

The Python code has been documented using docstrings, which is very convenient for user that want to either use
the software or develop new features and functionalities.

To see all the information for the different Python modules, classes, methods and all the possible configuration 
options, read the :doc:`pyNAVIS package section <pyNAVIS>`.



Contributing
============

If you would like to help improve ``pyNAVIS``, please read our :doc:`contributing guide <Contributing>`.

License
=======

This project is licensed under the GPL License - see the `LICENSE.md file <https://github.com/jpdominguez/pyNAVIS/blob/master/LICENSE>`__ for details.

For further information and help, please contact me at jpdominguez@atc.us.es.