pihdf: Python Hardware Design Framework based on MyHDL
======================================================

A very preliminary documentation (work-in-progress) is available at: http://hnikolov.github.io/pihdf_doc/

Install ``pihdf`` 
-----------------

To install ``pihdf`` in editable mode: ::

    $ sudo python setup.py develop

``pihdf`` depends on the following python packages: __myhdl, simplejson, coverage, nose__. 
These will be installed during the installation of `pihdf` if not present on your system. 

__Note:__ These packages will __not__ be un-installed if you un-install `pyhdf`. 


Un-install ``pihdf``
--------------------

To un-install ``pihdf``: ::

    $ sudo python setup.py develop --uninstall

Then, remove the command-line script ``module`` from its location: ::

    $ which module | xargs sudo rm


Co-simulation, waveform and dotty viewers
-----------------------------------------

For co-simulations, `pihdf` uses the __Icarus iverilog__ simulator. __GTKWave__ is the waveform viewer used in `pihdf`. For structured designs, `pihdf` generates also the design topology (i.e., HW modules interconnections) as a `.dot` file. To viasualize it, you can use `xdot` program. Install all programs by executing: ::

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

