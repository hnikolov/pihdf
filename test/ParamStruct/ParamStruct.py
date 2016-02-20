from myhdl import *
from pihdf import Convertible
from pihdf.interfaces import *

import sys
import os
module_path = os.path.dirname(__file__)

lib_path = os.path.abspath(module_path + "/../../Param")
sys.path.append(lib_path)

from src.ParamStruct_beh import *
from src.ParamStruct_rtl import *

class ParamStruct(Convertible):
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
            HSD(direction=self.OUT, name="tx", data=16, filedump=fdump)
        ]

        # no lambda here
        self.parameters = [
            Parameter("TOP_PARAM_NONE", value=None),
            Parameter("TOP_PARAM_BOOL", value=True),
            Parameter("TOP_PARAM_INT", value=10),
            Parameter("TOP_PARAM_FLOAT", value=1.5),
            Parameter("TOP_PARAM_STR", value='my_string_A')            
        ]

        # register implementations used in Convertible.gen()
        self.funcdict = {
            'beh': ParamStruct_beh,
            'rtl': ParamStruct_rtl,
            'vrg': None
        }


    def top(self,
            rst, clk,
            tx_ready,tx_valid,tx_data,
            TOP_PARAM_NONE, TOP_PARAM_BOOL, TOP_PARAM_INT, TOP_PARAM_FLOAT, TOP_PARAM_STR):
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

    dn = ParamStruct(IMPL=1)
    dn.convert(hdl="verilog", params={"TOP_PARAM_NONE":None, "TOP_PARAM_BOOL":True, "TOP_PARAM_INT":10, "TOP_PARAM_FLOAT":1.5, "TOP_PARAM_STR":'my_string_A'})
    dn.convert(hdl="vhdl", params={"TOP_PARAM_NONE":None, "TOP_PARAM_BOOL":True, "TOP_PARAM_INT":10, "TOP_PARAM_FLOAT":1.5, "TOP_PARAM_STR":'my_string_A'})
    dn.clean()
