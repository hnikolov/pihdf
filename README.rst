pihdf: Python Hardware Design Framework based on MyHDL
======================================================

A very preliminary documentation (work-in-progress) is available at: http://hnikolov.github.io/pyhdf_doc/

Note that the name "pyhdf_doc" has to be changed to "pihdf_doc".

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

Note
----

``pihdf`` requiers ``myhdl_lib`` (https://github.com/nkavaldj/myhdl_lib) 

``myhdl_lib`` requires ``scapy`` (http://www.secdev.org/projects/scapy/doc/installation.html)


