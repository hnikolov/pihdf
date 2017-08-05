from myhdl import *
from pihdf import *
from myhdl_lib import *

from modules.A.A import A
from modules.B.B import B
from modules.C.C import C

#--- Custom code begin ---#
#--- Custom code end   ---#

def AXI4SlaveRegFile_rtl(rst, clk, sbus, IMPL, FDUMP):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    sbus_waddr, sbus_wdata, sbus_wresp, sbus_raddr, sbus_rdata = sbus.interfaces()
    sbus_waddr_ready, sbus_waddr_valid, sbus_waddr_data = sbus_waddr.get_snk_signals() # consume data
    sbus_wdata_ready, sbus_wdata_valid, sbus_wdata_data, sbus_wdata_strobes = sbus_wdata.get_snk_signals() # consume data
    sbus_wresp_ready, sbus_wresp_valid, sbus_wresp_data = sbus_wresp.get_src_signals() # produce data
    sbus_raddr_ready, sbus_raddr_valid, sbus_raddr_data = sbus_raddr.get_snk_signals() # consume data
    sbus_rdata_ready, sbus_rdata_valid, sbus_rdata_data, sbus_rdata_response = sbus_rdata.get_src_signals() # produce data

    """ Local interfaces """

    if isinstance(IMPL, dict):
        A1_impl = IMPL["A1"] if "A1" in IMPL else IMPL["top"]
        A2_impl = IMPL["A2"] if "A2" in IMPL else IMPL["top"]
        B3_impl = IMPL["B3"] if "B3" in IMPL else IMPL["top"]
        C4_impl = IMPL["C4"] if "C4" in IMPL else IMPL["top"]
    else:
        A1_impl = IMPL
        A2_impl = IMPL
        B3_impl = IMPL
        C4_impl = IMPL

    """ Components """
    A1 = A(A1_impl).gen(clk=clk, rst=rst, sbus=sbus)
    A2 = A(A2_impl).gen(clk=clk, rst=rst, sbus=sbus)
    B3 = B(B3_impl).gen(clk=clk, rst=rst, sbus=sbus)
    C4 = C(C4_impl).gen(clk=clk, rst=rst, sbus=sbus)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
