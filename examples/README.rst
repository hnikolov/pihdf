pihdf examples
==============

Work-in-Progress...

This directory contains several HW module designs. The purpose of these designs is to illustrate different features of ``pihdf``
and to help you get started with ``pihdf``. 

``hsd``: Data communication in ``pihdf`` using Hand-Shake-Data interfaces
-------------------------------------------------------------------------

_TODO_: Add the example.
Data communication between HW modules, and between HW module and the tests bench in ``pihdf`` 
is based on hand-shake synchronization. Hand-shake is _native_ part of ``pihdf`` and the data interfaces it supports.
This is the first example you should start with. 

`myvrlg <https://github.com/hnikolov/pihdf/tree/master/examples/myvrlg>`_: HW Modules designed in Verilog
---------------------------------------------------------------------------------------------------------

Illustrates how to use ``pihdf`` for developing HW modules in **Verilog**.
Module implementation is given in RTL Verilog, while behavior model and tests are specified in python using ``pihdf``.


`hsd_custom <https://github.com/hnikolov/pihdf/tree/master/examples/hsd_custom>`_: User-defined data-fields interfaces
----------------------------------------------------------------------------------------------------------------------

User-defined data-fields interface used as hand-shake data (HSD) interface within ``pihdf``. 
The custom interface is defined in a .py file located in directory ``common``. The custom interface is used in file ``hsd_custom.json``, which
describes the HW module top-level interfaces.
