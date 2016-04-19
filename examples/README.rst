pihdf examples
==============

Work-in-Progress...

This directory contains several HW module designs. The purpose of these designs is to illustrate different features of ``pihdf``
and to help you getting started with ``pihdf``. 


`myvrlg <https://github.com/hnikolov/pihdf/tree/master/examples/myvrlg>`_
-------------------------------------------------------------------------

Illustrates how to use ``pihdf`` for developing HW modules in **Verilog**.
Module implementation is given in RTL Verilog, while tests are specified in python using ``pihdf``.


`hsd_custom <https://github.com/hnikolov/pihdf/tree/master/examples/hsd_custom>`_
---------------------------------------------------------------------------------

Use custom-defined data-fields interface as hand-shake data (HSD) interface within ``pihdf``. 
The custom interface is defined in a .py file located in directory ``common``. The custom interface is used in file ``hsd_custom.json``, which
describes the HW module top-level interfaces.
