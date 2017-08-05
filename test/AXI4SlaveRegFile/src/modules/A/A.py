from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.A_beh import *
from src.A_rtl import *

class A(Convertible):
    '''|
    | The design class
    |________'''
    def __init__(self, IMPL={}):

        self.structural = False

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
            AXI4Slave(bus_type=SBUS, name="sbus", reg_file=True, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': A_beh,
            'rtl': A_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            sbus_waddr_ready,sbus_waddr_valid,sbus_waddr_data,
            sbus_wdata_ready,sbus_wdata_valid,sbus_wdata_data,sbus_wdata_strobes,
            sbus_wresp_ready,sbus_wresp_valid,sbus_wresp_data,
            sbus_raddr_ready,sbus_raddr_valid,sbus_raddr_data,
            sbus_rdata_ready,sbus_rdata_valid,sbus_rdata_data,sbus_rdata_response):
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

    dn = A(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
