from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.TOut_beh import *
from src.TOut_rtl import *

class TOut(Convertible):
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
            HSD(direction=self.IN, name="mode", data=2, push=True, filedump=fdump),
            HSD(direction=self.IN, name="inc_in", data=2, filedump=fdump),
            HSD(direction=self.OUT, name="LEDs", data=5, filedump=fdump),
            HSD(direction=self.OUT, name="rdy_out", data=1, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': TOut_beh,
            'rtl': TOut_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            mode_ready,mode_valid,mode_data,
            inc_in_ready,inc_in_valid,inc_in_data,
            LEDs_ready,LEDs_valid,LEDs_data,
            rdy_out_ready,rdy_out_valid,rdy_out_data):
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

    dn = TOut(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
