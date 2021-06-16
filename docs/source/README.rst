
********
pyNAVIS
********


.. image:: https://img.shields.io/pypi/v/pyNAVIS.svg
   :target: https://pypi.python.org/pypi/pyNAVIS
   :alt: Pypi Version 
.. image:: https://img.shields.io/pypi/l/pyNAVIS.svg
   :target: https://pypi.python.org/pypi/pyNAVIS/
   :alt: License
.. image:: https://readthedocs.org/projects/pynavis/badge/?version=latest
   :target: https://pynavis.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status




``pyNAVIS`` is an open-source cross-platform Python module for analyzing and processing spiking information obtained from neuromorphic auditory sensors. It is primarily focused to be used with a NAS_, but can work with any other cochlea sensor.



For more information, head over to the `Github repository <https://github.com/jpdominguez/pyNAVIS>`_.

.. _NAS: https://github.com/RTC-research-group/OpenNAS

Installing
==========

``pyNAVIS`` is distributed on PyPI_ and can be installed with pip:

.. prompt:: bash $

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

The Python code has been documented using docstrings, which is very convenient for users that want to either use
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


Cite this work
==============

``APA`` Dominguez-Morales, J. P., Gutierrez-Galan, D., Rios-Navarro, A., Duran-Lopez, L., Dominguez-Morales, M., & Jimenez-Fernandez, A. (2021). pyNAVIS: An open-source cross-platform software for spike-based neuromorphic audio information processing. Neurocomputing, 449, 172-175.

``ISO 690`` DOMINGUEZ-MORALES, Juan P., et al. pyNAVIS: An open-source cross-platform software for spike-based neuromorphic audio information processing. Neurocomputing, 2021, vol. 449, p. 172-175.

``MLA`` Dominguez-Morales, Juan P., et al. "pyNAVIS: An open-source cross-platform software for spike-based neuromorphic audio information processing." Neurocomputing 449 (2021): 172-175.

``BibTeX`` @article{dominguez2021pynavis, title={pyNAVIS: An open-source cross-platform software for spike-based neuromorphic audio information processing}, author={Dominguez-Morales, Juan P and Gutierrez-Galan, D and Rios-Navarro, A and Duran-Lopez, L and Dominguez-Morales, M and Jimenez-Fernandez, A}, journal={Neurocomputing}, volume={449}, pages={172--175}, year={2021}, publisher={Elsevier} }