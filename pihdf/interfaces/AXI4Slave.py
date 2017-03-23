from myhdl import *
from Bus   import Bus
from HSD   import HSD

class AXI4Slave(Bus):
    '''|
    | TODO
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2): # TODO bus_type to be removed
                     
        axi4slave_ifs = lambda : [] # TODO
                  
        # invoke base class constructor
        Bus.__init__(self, bus_type=axi4slave_ifs, name=name, reg_file=reg_file, filedump=filedump, lo=-3)

