from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def hsd_inc_rtl(rst, clk, rxd, txd):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    rxd_ready, rxd_valid, rxd_data = rxd.get_snk_signals() # consume data
    txd_ready, txd_valid, txd_data = txd.get_src_signals() # produce data

    #--- Custom code begin ---#
    hsd_en = Signal(bool(0))

    hsd_en_inst = rxd.enable(rst, clk, txd_ready, txd_valid, hsd_en)

    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_hs():
        if hsd_en:
            txd_data.next = rxd_data + 1

    #--- Custom code end   ---#

    return all_instances(rst, clk)
