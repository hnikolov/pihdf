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
    sbus_wa_wd, sbus_raddr, sbus_rdata = sbus.interfaces()
    sbus_wa_wd_ready, sbus_wa_wd_valid, sbus_wa_wd_addr, sbus_wa_wd_data = sbus_wa_wd.get_snk_signals() # consume data
    sbus_raddr_ready, sbus_raddr_valid, sbus_raddr_data = sbus_raddr.get_snk_signals() # consume data
    sbus_rdata_ready, sbus_rdata_valid, sbus_rdata_data = sbus_rdata.get_src_signals() # produce data

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
