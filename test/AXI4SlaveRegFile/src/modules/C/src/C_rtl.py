from myhdl import *
from pihdf import *
from myhdl_lib import *

from B.B import B

#--- Custom code begin ---#
#--- Custom code end   ---#

def C_rtl(rst, clk, sbus, IMPL, FDUMP):
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
        B1_impl = IMPL["B1"] if "B1" in IMPL else IMPL["top"]
    else:
        B1_impl = IMPL

    """ Components """
    B1 = B(B1_impl).gen(clk=clk, rst=rst, sbus=sbus)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
