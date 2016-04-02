from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

import sys
import os
module_path = os.path.dirname(__file__)


import site
site.addsitedir(module_path + '/src/modules')

from src.RegFile_tb_beh import *
from src.RegFile_tb_rtl import *

class RegFile_tb(Convertible):
    '''|
    | The design class
    |________'''
    def __init__(self, IMPL={}):

        self.structural = True
        self.models = IMPL

        if isinstance(IMPL, dict):
            self.IMPL = IMPL["top"] if "top" in IMPL else IMPL
        else:
            self.IMPL = IMPL

        # call base class constructor
        Convertible.__init__(self)

        self.resets = lambda : [
            Reset(name="rst", active=1, val=1, async=True)
        ]

        self.clocks = lambda : [
            Clock(name="clk")
        ]

        self.interfaces = lambda fdump : [
            Bus(bus_type=SBUS, name="simple_bus", reg_file=True, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': RegFile_tb_beh,
            'rtl': RegFile_tb_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            simple_bus_wa_wd_ready,simple_bus_wa_wd_valid,simple_bus_wa_wd_addr,simple_bus_wa_wd_data,
            simple_bus_raddr_ready,simple_bus_raddr_valid,simple_bus_raddr_data,
            simple_bus_rdata_ready,simple_bus_rdata_valid,simple_bus_rdata_data):
        '''|
        | Provides flat interface to the top-level implementation. This
        | function is given to MyHDL.toVerilog() and MyHDL.toVHDL()
        |________'''
        x = locals()
        del x['self']
        return self.flat2struct(**x)


if __name__ == "__main__":

    import myhdl
    import pihdf

    pihdf.info("Using MyHDL version %s" % myhdl.__version__)
    pihdf.info("Using MyFramework version %s" % pihdf.__version__)

    dn = RegFile_tb(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
