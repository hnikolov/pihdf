from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

from Param.Param import Param

#--- Custom code begin ---#
#--- Custom code end   ---#

def ParamStruct_rtl(rst, clk, tx, TOP_PARAM_NONE, TOP_PARAM_BOOL, TOP_PARAM_INT, TOP_PARAM_FLOAT, TOP_PARAM_STR, IMPL, FDUMP):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    tx_ready, tx_valid, tx_data = tx.get_src_signals() # produce data

    """ Local interfaces """

    # Parameters
    LOC_PARAM_NONE = None
    LOC_PARAM_BOOL = False
    LOC_PARAM_INT = 20
    LOC_PARAM_FLOAT = 2.5
    LOC_PARAM_STR = 'my_string_B'

    if isinstance(IMPL, dict):
        my_submodule_loc_impl = IMPL["my_submodule_loc"] if "my_submodule_loc" in IMPL else IMPL["top"]
        my_submodule_top_impl = IMPL["my_submodule_top"] if "my_submodule_top" in IMPL else IMPL["top"]
    else:
        my_submodule_loc_impl = IMPL
        my_submodule_top_impl = IMPL

    """ Components """
    my_submodule_loc = Param(my_submodule_loc_impl).gen(PARAM_FLOAT=LOC_PARAM_FLOAT, tx=tx, clk=clk, PARAM_BOOL=LOC_PARAM_BOOL, PARAM_NONE=LOC_PARAM_NONE, PARAM_INT=LOC_PARAM_INT, PARAM_STR=LOC_PARAM_STR, rst=rst)
    my_submodule_top = Param(my_submodule_top_impl).gen(PARAM_FLOAT=TOP_PARAM_FLOAT, tx=tx, clk=clk, PARAM_BOOL=TOP_PARAM_BOOL, PARAM_NONE=TOP_PARAM_NONE, PARAM_INT=TOP_PARAM_INT, PARAM_STR=TOP_PARAM_STR, rst=rst)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
