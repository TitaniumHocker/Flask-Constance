Installation
============

Python Version
--------------

Flask-Constance supports Python 3.6 and newer. The choice of the 
minimum version is due to the fact that the author needs to support 
several applications that work only on this version. Until this 
changes, the minimum version will not be increased.

Dependencies
------------

The only required dependency of this extension is Flask.
However, to use the various backends, one way or another, 
you will need to install additional packages. They are 
defined through optional dependencies.

The following optional dependencies are currently available:

- **[fsqla]** - for Flask-SQLAlchemy backend.

Installation from PyPI
----------------------

This is the most common way to install Flask-Constance package.

.. code:: bash
    
   python3 -m pip install flask-constance

And this is command to install package with optional dependencies
related to Flask-SQLAlchemy backend.

.. code:: bash

   python3 -m pip install flask-constance[fsqla]


Building from source
--------------------

To install a package from source, you first need 
to clone the repository.To install package from source.

.. code:: bash

    git clone https://github.com/TitaniumHocker/Flask-Constance.git Flask-Constance

Then you can install it with pip.

.. code:: bash

    pytho3 -m pip install ./Flask-Constance


Signalling support
------------------

If you wish to use Flask-Constance signals,
ensure that `blinker` package is installed.

.. code:: bash

    python3 -m pip install blinker
    