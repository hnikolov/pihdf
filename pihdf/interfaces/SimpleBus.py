from myhdl import *
from Bus import Bus
from HSD import HSD

class SimpleBus(Bus):
    '''|
    | TODO
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2):
        
        wd_fields = [("addr", intbv(0)[ 8:]),
                     ("data", intbv(0)[32:])]
             
        sbus_ifs = lambda : [ HSD(direction = 0, name = "wa_wd", data = wd_fields),
                              HSD(direction = 0, name = "raddr", data =  8),
                              HSD(direction = 1, name = "rdata", data = 32)]
                  
        # invoke base class constructor
        Bus.__init__(self, bus_type=sbus_ifs, name=name, reg_file=reg_file, filedump=filedump, lo=-3)

