from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.tsched_beh import *
from src.tsched_rtl import *

class tsched(Convertible):
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
            HSD(direction=self.IN, name="rx_port", data=port_fields, push=False, filedump=fdump),
            HSD(direction=self.OUT, name="tx_port", data=port_fields, push=False, filedump=fdump),
            STAvln(data_width=64, direction=self.IN, name="rx", filedump=fdump),
            STAvln(data_width=64, direction=self.OUT, name="tx", filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': tsched_beh,
            'rtl': tsched_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            rx_port_ready,rx_port_valid,rx_port_cmd,rx_port_port,
            tx_port_ready,tx_port_valid,tx_port_cmd,tx_port_port,
            rx_ready,rx_valid,rx_sop,rx_eop,rx_empty,rx_data,rx_err,
            tx_ready,tx_valid,tx_sop,tx_eop,tx_empty,tx_data,tx_err):
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

    dn = tsched(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
