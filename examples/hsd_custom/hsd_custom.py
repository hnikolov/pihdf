from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from interfaces import *

from src.hsd_custom_beh import *
from src.hsd_custom_rtl import *

class hsd_custom(Convertible):
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
            HSD(direction=self.IN, name="rx_port_flds", data=my_port_fields, filedump=fdump),
            HSD(direction=self.OUT, name="tx_port_flds", data=my_port_fields, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': hsd_custom_beh,
            'rtl': hsd_custom_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            rx_port_flds_ready,rx_port_flds_valid,rx_port_flds_cmd,rx_port_flds_port,
            tx_port_flds_ready,tx_port_flds_valid,tx_port_flds_cmd,tx_port_flds_port):
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

    dn = hsd_custom(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
