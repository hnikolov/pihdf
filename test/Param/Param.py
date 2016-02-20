from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

from src.Param_beh import *
from src.Param_rtl import *

class Param(Convertible):
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
            HSD(direction=self.OUT, name="tx", data=16, filedump=fdump)
        ]

        # no lambda here
        self.parameters = [
            Parameter("PARAM_NONE", value=None),
            Parameter("PARAM_BOOL", value=True),
            Parameter("PARAM_INT", value=10),
            Parameter("PARAM_FLOAT", value=1.5),
            Parameter("PARAM_STR", value='my_string_A')            
        ]

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': Param_beh,
            'rtl': Param_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            tx_ready,tx_valid,tx_data,
            PARAM_NONE, PARAM_BOOL, PARAM_INT, PARAM_FLOAT, PARAM_STR):
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

    dn = Param(IMPL=1)
    dn.convert(hdl="verilog", params={"PARAM_NONE":None, "PARAM_BOOL":True, "PARAM_INT":10, "PARAM_FLOAT":1.5, "PARAM_STR":'my_string_A'})
    dn.convert(hdl="vhdl", params={"PARAM_NONE":None, "PARAM_BOOL":True, "PARAM_INT":10, "PARAM_FLOAT":1.5, "PARAM_STR":'my_string_A'})
    dn.clean()
