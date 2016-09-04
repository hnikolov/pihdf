from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def TIncr_rtl(rst, clk, mode, inc_out, rdy_en, rdy_buff):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    mode_ready, mode_valid, mode_data = mode.get_snk_signals() # consume data
    inc_out_ready, inc_out_valid, inc_out_data = inc_out.get_src_signals() # produce data
    rdy_en_ready, rdy_en_valid, rdy_en_data = rdy_en.get_src_signals() # produce data
    rdy_buff_ready, rdy_buff_valid, rdy_buff_data = rdy_buff.get_src_signals() # produce data

    #--- Custom code begin ---#

    hsd_en = Signal(bool(0))

    hsd_en_inst = mode.enable(rst, clk, inc_out_ready, inc_out_valid, hsd_en)

    count = Signal(modbv(0, min=0, max=2**32)) # should have full bit vector range

    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_hs():
        if hsd_en:           
#            count.next = (inc_out_data + 1) % 3 # in case of custom range
            count.next = count + 1

            if mode_data == 1:
#                count.next = (inc_out_data + 2) % 3
                count.next = count + 2         

    @always_comb
    def out_prcs():
        rdy_en_data.next   = mode_valid
        rdy_buff_data.next = inc_out_ready
        inc_out_data.next  = count[2:0]
#        inc_out_data.next  = count[26:24] # for synthesis

    #--- Custom code end   ---#

    return all_instances(rst, clk)
