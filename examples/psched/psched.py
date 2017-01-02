from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.psched_beh import *
from src.psched_rtl import *

class psched(Convertible):
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
            HSD(direction=self.OUT, name="sequence", data=8, filedump=fdump),
            STAvln(data_width=64, direction=self.IN, name="rx", filedump=fdump),
            STAvln(data_width=64, direction=self.OUT, name="tx", filedump=fdump)
        ]

        # no lambda here
        self.parameters = [
            Parameter("SEQ_RX", value=False),
            Parameter("SEQ_RX_PORT", value=False),
            Parameter("SEQ_TX", value=False),
            Parameter("SEQ_TX_PORT", value=False)            
        ]

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': psched_beh,
            'rtl': psched_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            rx_port_ready,rx_port_valid,rx_port_cmd,rx_port_port,
            tx_port_ready,tx_port_valid,tx_port_cmd,tx_port_port,
            sequence_ready,sequence_valid,sequence_data,
            rx_ready,rx_valid,rx_sop,rx_eop,rx_empty,rx_data,rx_err,
            tx_ready,tx_valid,tx_sop,tx_eop,tx_empty,tx_data,tx_err,
            SEQ_RX, SEQ_RX_PORT, SEQ_TX, SEQ_TX_PORT):
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

    dn = psched(IMPL=1)
    dn.convert(hdl="verilog", params={"SEQ_RX":False, "SEQ_RX_PORT":False, "SEQ_TX":False, "SEQ_TX_PORT":False})
    dn.convert(hdl="vhdl", params={"SEQ_RX":False, "SEQ_RX_PORT":False, "SEQ_TX":False, "SEQ_TX_PORT":False})
    dn.clean()
