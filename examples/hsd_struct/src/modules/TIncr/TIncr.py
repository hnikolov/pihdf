from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.TIncr_beh import *
from src.TIncr_rtl import *

class TIncr(Convertible):
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
            HSD(direction=self.IN, name="mode", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="inc_out", data=2, filedump=fdump),
            HSD(direction=self.OUT, name="rdy_en", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="rdy_buff", data=1, filedump=fdump)
        ]

        # no lambda here
        self.parameters = [
            Parameter("DELAY_BITS", value=24)            
        ]

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': TIncr_beh,
            'rtl': TIncr_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            mode_ready,mode_valid,mode_data,
            inc_out_ready,inc_out_valid,inc_out_data,
            rdy_en_ready,rdy_en_valid,rdy_en_data,
            rdy_buff_ready,rdy_buff_valid,rdy_buff_data,
            DELAY_BITS):
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

    dn = TIncr(IMPL=1)
    dn.convert(hdl="verilog", params={"DELAY_BITS":24})
    dn.convert(hdl="vhdl", params={"DELAY_BITS":24})
    dn.clean()
