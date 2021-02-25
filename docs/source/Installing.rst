**********
Installing
**********

This section describes how to install and set up ``pyNAVIS``.

First, some :ref:`requirements <requirements>` need to be installed. If you already have a running Python3 environment, 
you can skip this step and move either to the :ref:`User Installation <user_install>` or to the :ref:`Developer Installation <dev_install>`.




 .. _requirements:
 
Requirements
================

``pyNAVIS`` runs under Python3, so first you need to install and set up a Python3 environment.


For doing so, we recommend using Anaconda, which is a free and open-source distribution of the Python and R 
programming languages that aims to simplify package management and deployment. We recommend installing Anaconda 3.7, 
which can be downloaded from `their website <https://www.anaconda.com/distribution/>`_.


After installing Anaconda, let's create a new Python environment, which is a directory that contains a specific collection of conda packages.

.. note::
   Creating a Python environment is not necessary, but it is highly recommended. Environments act as a sand box where you can install and play around without spoiling the base Python installation. 


For creating a Python environment, open a terminal (or the Anaconda Prompt if you are using Windows) and run:

.. prompt:: bash $

   conda create -n pyNAVIS_env python=3.7

Where pyNAVIS_env is the name of the environment and can be changed to your liking. After that, activate your environment by doing:

.. prompt:: bash $

   conda activate pyNAVIS_env

.. note::
   `Spyder <https://www.spyder-ide.org/>`_, which is a well-known Python IDE is installed together with Anaconda.


After that, head over to the :ref:`User Installation <user_install>` or to the :ref:`Developer Installation <dev_install>` instructions.







.. _user_install:
 
User installation
=================

To install ``pyNAVIS``, run the following line in the terminal:

.. prompt:: bash $

   pip install pyNAVIS

This will automatically install all the dependencies needed to use this package, which are ``numpy``, ``scipy`` and ``matplotlib``.

You can now start using ``pyNAVIS``. Head over to the :doc:`Getting Started section <Getting started>` to introduce you to its functionalities and how to use it. Some other useful commands can be seen in the following note:

.. note::
   To update pyNAVIS to the latest version, use the following command:

   .. prompt:: bash $

      pip install --upgrade pyNAVIS

   To install a specific version of pyNAVIS use the following command:

   .. prompt:: bash $

      pip install pyNAVIS==version

   To upgrade an already installed pyNAVIS package to the latest from PyPi use the following command:

   .. prompt:: bash $

      pip install --upgrade pyNAVIS

   To uninstall pyNAVIS use the following command:

   .. prompt:: bash $

      pip uninstall pyNAVIS

.. _dev_install:
 
Developer installation
======================

Clone or download `the repository <https://github.com/jpdominguez/pyNAVIS>`_. After that, head to: 

.. prompt:: bash $
   
   cd /path/to/project/src

And run the following line from your terminal to install all the dependencies:

.. prompt:: bash $

   pip install -r requirements.txt


.. note::
   Now you have everything set up to code. Take a look at the ``main.py`` file and the examples under the ``/examples`` folder to familiarize with ``pyNAVIS``.
   Also, don't forget to take a look at the :doc:`pyNAVIS package section <pyNAVIS>`, which has all the information about classes and methods.

.. warning::
   If you want to add new functionalities to ``pyNAVIS``, please visit the :doc:`Contributing section <Contributing>`.