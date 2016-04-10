pihdf: Python Hardware Design Framework based on MyHDL
======================================================

.. image:: https://travis-ci.org/hnikolov/pihdf.svg?branch=master
  :target: https://travis-ci.org/hnikolov/pihdf

A very preliminary documentation (work-in-progress) is available at: http://hnikolov.github.io/pihdf_doc/


Install `pihdf` using pip
-------------------------

You can install the latest release of `pihdf` from pypi: ::

	$ sudo pip install pihdf

**Note:** If you do not have `pip` installed: ::

	$ sudo apt-get install python-pip python-dev build-essential 
	$ sudo pip install --upgrade pip 


Install `pihdf` from source
---------------------------

If you plan to contribute to `pihdf`, then install it from source: ::

	$ git clone https://github.com/hnikolov/pihdf
	$ cd pihdf
	$ sudo python setup.py develop

Option `develop` installs `pyhdf` in *editable* mode. 
This is very convenient because your changes are immediately reflected into the installed `pihdf` package.
This means that you do not need to re-install `pihdf` in order your changes to take effect.


Dependences on Python packages
------------------------------

`pihdf` requires the following python packages: **myhdl, myhdl_lib, simplejson, coverage, nose**. 
These packages will be installed during the installation of `pihdf` if not present on your system. 

**Note:** These packages will **not** be un-installed if you un-install `pyhdf`. 


Co-simulation, waveform and dotty viewers
-----------------------------------------

For co-simulations, `pihdf` uses the **Icarus iverilog** simulator. **GTKWave** is the waveform viewer used in `pihdf`. For structured designs, `pihdf` generates also the design topology (i.e., HW modules interconnections) as a `.dot` file. To viasualize it, you can use `xdot` program. Install all programs by executing: ::

    $ sudo apt-get install iverilog gtkwave xdot


Create `myhdl.vpi`
------------------

For co-simuations, myhdl uses a `.vpi` interface. To create the `myhdl.vpi` file used with __Icarus__, you need the source of `myhdl`: ::

	$ git clone https://github.com/jandecaluwe/myhdl
	$ make -C myhdl/cosimulation/icarus
	$ sudo mkdir /.pihdf
	$ sudo cp myhdl/cosimulation/icarus/myhdl.vpi /.pihdf

**Note:** `pihdf` expects file `myhdl.vpi` to be in folder `/.pihdf`


Un-install
----------

Un-installing `pihdf` (should you decide to do so) is easy. Depending on how you installed it, you can:

Un-install `pihdf` using pip ::

	$ sudo pip uninstall pihdf

Or, un-install `pihdf` if installed from source ::

	$ cd pihdf
	$ sudo python setup.py develop --uninstall


Remove `module`
---------------

To remove the command-line tool `module` from its location: ::

	$ which module | xargs sudo rm


Note
----

The command-line tool ``module`` makes use of the very convenient package ``docopt`` (https://github.com/docopt/docopt), which is copied in the ``pihdf`` repository.
