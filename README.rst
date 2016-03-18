pihdf: Python Hardware Design Framework based on MyHDL
======================================================

.. image:: https://travis-ci.org/hnikolov/pihdf.svg?branch=master
  :target: https://travis-ci.org/hnikolov/pihdf

A very preliminary documentation (work-in-progress) is available at: http://hnikolov.github.io/pihdf_doc/

Install ``pihdf`` 
-----------------

To install ``pihdf`` in editable mode: ::

    $ sudo python setup.py develop

``pihdf`` depends on the following python packages: **myhdl, simplejson, coverage, nose**. 
These will be installed during the installation of `pihdf` if not present on your system. 

**Note:** These packages will **not** be un-installed if you un-install `pyhdf`. 


Un-install ``pihdf``
--------------------

To un-install ``pihdf``: ::

    $ sudo python setup.py develop --uninstall

Then, remove the command-line script ``module`` from its location: ::

    $ which module | xargs sudo rm


Co-simulation, waveform and dotty viewers
-----------------------------------------

For co-simulations, `pihdf` uses the **Icarus iverilog** simulator. **GTKWave** is the waveform viewer used in `pihdf`. For structured designs, `pihdf` generates also the design topology (i.e., HW modules interconnections) as a `.dot` file. To viasualize it, you can use `xdot` program. Install all programs by executing: ::

    $ sudo apt-get install iverilog gtkwave xdot


Create `myhdl.vpi`
------------------

For co-simuations, myhdl uses a `.vpi` interface. To create the `myhdl.vpi` file used with Icarus, download the source of myhdl. Then, ::

    $ cd [myhdl-folder]/cosimulation/icarus/
    $ make 
 

Make sure that file ``myhdl.vpi`` is copied to directory ``/.pihdf``!


Notes
-----

``pihdf`` requiers ``myhdl_lib`` (https://github.com/nkavaldj/myhdl_lib) 

The command-line tool ``module`` makes use of the very convenient package ``docopt`` (https://github.com/docopt/docopt), which is copied in the ``pihdf`` repository.

