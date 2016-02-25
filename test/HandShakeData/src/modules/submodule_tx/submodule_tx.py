from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.submodule_tx_beh import *
from src.submodule_tx_rtl import *

class submodule_tx(Convertible):
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
            HSD(direction=self.IN, name="rx_width", data=64, filedump=fdump),
            HSD(direction=self.OUT, name="tx_width", data=64, filedump=fdump),
            HSD(direction=self.IN, name="rx_width1", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="tx_width1", data=1, filedump=fdump),
            HSD(direction=self.IN, name="rx_fields", data=test_fields, filedump=fdump),
            HSD(direction=self.OUT, name="tx_fields", data=test_fields, filedump=fdump),
            HSD(direction=self.IN, name="rx_width_buf", data=64, filedump=fdump),
            HSD(direction=self.OUT, name="tx_width_buf", data=64, filedump=fdump),
            HSD(direction=self.IN, name="rx_width1_buf", data=1, filedump=fdump),
            HSD(direction=self.OUT, name="tx_width1_buf", data=1, filedump=fdump),
            HSD(direction=self.IN, name="rx_fields_buf", data=test_fields, filedump=fdump),
            HSD(direction=self.OUT, name="tx_fields_buf", data=test_fields, filedump=fdump),
            HSD(direction=self.IN, name="rx_fields_const", data=test_fields, filedump=fdump),
            HSD(direction=self.OUT, name="tx_fields_const", data=test_fields, filedump=fdump),
            HSD(direction=self.OUT, name="tx_pull", data=64, filedump=fdump),
            HSD(direction=self.IN, name="rx_terminate", data=64, filedump=fdump),
            HSD(direction=self.OUT, name="tx_terminate", data=64, filedump=fdump),
            HSD(direction=self.OUT, name="ipg_tx_width", data=16, filedump=fdump)
        ]

        self.parameters = []

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': submodule_tx_beh,
            'rtl': submodule_tx_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            rx_width_ready,rx_width_valid,rx_width_data,
            tx_width_ready,tx_width_valid,tx_width_data,
            rx_width1_ready,rx_width1_valid,rx_width1_data,
            tx_width1_ready,tx_width1_valid,tx_width1_data,
            rx_fields_ready,rx_fields_valid,rx_fields_bit,rx_fields_byte,rx_fields_word,
            tx_fields_ready,tx_fields_valid,tx_fields_bit,tx_fields_byte,tx_fields_word,
            rx_width_buf_ready,rx_width_buf_valid,rx_width_buf_data,
            tx_width_buf_ready,tx_width_buf_valid,tx_width_buf_data,
            rx_width1_buf_ready,rx_width1_buf_valid,rx_width1_buf_data,
            tx_width1_buf_ready,tx_width1_buf_valid,tx_width1_buf_data,
            rx_fields_buf_ready,rx_fields_buf_valid,rx_fields_buf_bit,rx_fields_buf_byte,rx_fields_buf_word,
            tx_fields_buf_ready,tx_fields_buf_valid,tx_fields_buf_bit,tx_fields_buf_byte,tx_fields_buf_word,
            rx_fields_const_ready,rx_fields_const_valid,rx_fields_const_bit,rx_fields_const_byte,rx_fields_const_word,
            tx_fields_const_ready,tx_fields_const_valid,tx_fields_const_bit,tx_fields_const_byte,tx_fields_const_word,
            tx_pull_ready,tx_pull_valid,tx_pull_data,
            rx_terminate_ready,rx_terminate_valid,rx_terminate_data,
            tx_terminate_ready,tx_terminate_valid,tx_terminate_data,
            ipg_tx_width_ready,ipg_tx_width_valid,ipg_tx_width_data):
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

    dn = submodule_tx(IMPL=1)
    dn.convert(hdl="verilog")
    dn.convert(hdl="vhdl")
    dn.clean()
