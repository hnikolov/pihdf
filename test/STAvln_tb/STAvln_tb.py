from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.STAvln_tb_beh import *
from src.STAvln_tb_rtl import *

class STAvln_tb(Convertible):
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
            STAvln(data_width=16, direction=self.IN, name="rx16", filedump=fdump),
            STAvln(data_width=16, direction=self.OUT, name="tx16", filedump=fdump),
            STAvln(data_width=32, direction=self.IN, name="rx32", filedump=fdump),
            STAvln(data_width=32, direction=self.OUT, name="tx32", filedump=fdump),
            STAvln(data_width=64, direction=self.IN, name="rx64", filedump=fdump),
            STAvln(data_width=64, direction=self.OUT, name="tx64", filedump=fdump),
            HSD(direction=self.OUT, name="ipg_rx16", data=16, filedump=fdump),
            HSD(direction=self.OUT, name="ipg_tx16", data=16, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': STAvln_tb_beh,
            'rtl': STAvln_tb_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            rx16_ready,rx16_valid,rx16_sop,rx16_eop,rx16_empty,rx16_data,rx16_err,
            tx16_ready,tx16_valid,tx16_sop,tx16_eop,tx16_empty,tx16_data,tx16_err,
            rx32_ready,rx32_valid,rx32_sop,rx32_eop,rx32_empty,rx32_data,rx32_err,
            tx32_ready,tx32_valid,tx32_sop,tx32_eop,tx32_empty,tx32_data,tx32_err,
            rx64_ready,rx64_valid,rx64_sop,rx64_eop,rx64_empty,rx64_data,rx64_err,
            tx64_ready,tx64_valid,tx64_sop,tx64_eop,tx64_empty,tx64_data,tx64_err,
            ipg_rx16_ready,ipg_rx16_valid,ipg_rx16_data,
            ipg_tx16_ready,ipg_tx16_valid,ipg_tx16_data):
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

    dn = STAvln_tb(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
