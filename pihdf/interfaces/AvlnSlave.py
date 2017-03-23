from myhdl import *
from Bus   import Bus
from HSD   import HSD

class AvlnSlave(Bus):
    '''|
    | TODO
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2): # TODO bus_type to be removed
                     
        avlnslave_ifs = lambda : [] # TODO
                  
        # invoke base class constructor
        Bus.__init__(self, bus_type=avlnslave_ifs, name=name, reg_file=reg_file, filedump=filedump, lo=-3)

