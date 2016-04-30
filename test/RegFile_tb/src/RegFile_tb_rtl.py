from myhdl import *
from pihdf import *
from myhdl_lib import *

from modules.A.A import A
from modules.B.B import B
from modules.C.C import C

#--- Custom code begin ---#
#--- Custom code end   ---#

def RegFile_tb_rtl(rst, clk, simple_bus, IMPL, FDUMP):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    simple_bus_wa_wd, simple_bus_raddr, simple_bus_rdata = simple_bus.interfaces()
    simple_bus_wa_wd_ready, simple_bus_wa_wd_valid, simple_bus_wa_wd_addr, simple_bus_wa_wd_data = simple_bus_wa_wd.get_snk_signals() # consume data
    simple_bus_raddr_ready, simple_bus_raddr_valid, simple_bus_raddr_data = simple_bus_raddr.get_snk_signals() # consume data
    simple_bus_rdata_ready, simple_bus_rdata_valid, simple_bus_rdata_data = simple_bus_rdata.get_src_signals() # produce data

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
    A1 = A(A1_impl).gen(clk=clk, rst=rst, sbus=simple_bus)
    A2 = A(A2_impl).gen(clk=clk, rst=rst, sbus=simple_bus)
    B3 = B(B3_impl).gen(clk=clk, rst=rst, sbus=simple_bus)
    C4 = C(C4_impl).gen(clk=clk, rst=rst, sbus=simple_bus)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
