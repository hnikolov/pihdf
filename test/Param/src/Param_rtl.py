from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def Param_rtl(rst, clk, tx, PARAM_NONE, PARAM_BOOL, PARAM_INT, PARAM_FLOAT, PARAM_STR):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    tx_ready, tx_valid, tx_data = tx.get_src_signals() # produce data

    #--- Custom code begin ---#
    assert isinstance(PARAM_NONE,   type(None)), "Parameter {} type error: expected type {}, detected type {}".format("PARAM_NONE", type(None), type(PARAM_NONE))
    assert isinstance(PARAM_BOOL,   bool), "Parameter {} type error: expected type {}, detected type {}".format("PARAM_BOOL", type(True), type(PARAM_BOOL))
    assert isinstance(PARAM_INT,    int), "Parameter {} type error: expected type {}, detected type {}".format("PARAM_INT", type(10), type(PARAM_INT))
    assert isinstance(PARAM_FLOAT,  float), "Parameter {} type error: expected type {}, detected type {}".format("PARAM_FLOAT", type(1.5), type(PARAM_FLOAT))
    assert isinstance(PARAM_STR,    str), "Parameter {} type error: expected type {}, detected type {}".format("PARAM_STR", type("1.5"), type(PARAM_STR))

    if PARAM_BOOL:
        # Default
        assert PARAM_NONE==None, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_NONE", None, PARAM_NONE)
        assert PARAM_BOOL==True, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_BOOL", True, PARAM_BOOL)
        assert PARAM_INT==10, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_INT", 10, PARAM_INT)
        assert PARAM_FLOAT==1.5, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_FLOAT", 1.5, PARAM_FLOAT)
        assert PARAM_STR=="my_string_A", "Parameter {} value error: expected value {}, detected value {}".format("PARAM_STR", "my_string_A", PARAM_STR)
    else:
        # Explicitly set in unit test or in structural design as local parameter
        assert PARAM_NONE==None, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_NONE", None, PARAM_NONE)
        assert PARAM_BOOL==False, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_BOOL", False, PARAM_BOOL)
        assert PARAM_INT==20, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_INT", 20, PARAM_INT)
        assert PARAM_FLOAT==2.5, "Parameter {} value error: expected value {}, detected value {}".format("PARAM_FLOAT", 2.5, PARAM_FLOAT)
        assert PARAM_STR=="my_string_B", "Parameter {} value error: expected value {}, detected value {}".format("PARAM_STR", "my_string_B", PARAM_STR)
    #--- Custom code end   ---#

    return all_instances(rst, clk)
