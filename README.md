# pihdf
Python Hardware Design Framework based on MyHDL
===============================================

Install ``pihdf`` 
-----------------

To install ``pihdf`` in editable mode: ::

    sudo python setup.py develop

Make sure that file ``myhdl.vpi`` is located in directory ``/.pihdf``!


Un-install `pihdf`
------------------------

To un-install ``pihdf``: ::

    sudo python setup.py develop --uninstall

Then, remove the command-line script ``module`` from its location: ::

    which module | xargs sudo rm
