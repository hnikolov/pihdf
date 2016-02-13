pihdf: Python Hardware Design Framework based on MyHDL
======================================================

A very preliminary documentation (work-in-progress) is available at: http://hnikolov.github.io/pihdf_doc/

Install ``pihdf`` 
-----------------

To install ``pihdf`` in editable mode: ::

    sudo python setup.py develop

Make sure that file ``myhdl.vpi`` is located in directory ``/.pihdf``!


Un-install ``pihdf``
------------------------

To un-install ``pihdf``: ::

    sudo python setup.py develop --uninstall

Then, remove the command-line script ``module`` from its location: ::

    which module | xargs sudo rm

Notes
-----

``pihdf`` requiers ``myhdl_lib`` (https://github.com/nkavaldj/myhdl_lib) 

``myhdl_lib`` requires ``scapy`` (http://www.secdev.org/projects/scapy/doc/installation.html)

The command-line tool ``module`` makes use of the very convenient package ``docopt`` (https://github.com/docopt/docopt), which is copied in the ``pihdf`` repository.


