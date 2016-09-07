from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def TIncr_rtl(rst, clk, mode, inc_out, rdy_en, rdy_buff, DELAY_BITS):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    mode_ready, mode_valid, mode_data = mode.get_snk_signals() # consume data
    inc_out_ready, inc_out_valid, inc_out_data = inc_out.get_src_signals() # produce data
    rdy_en_ready, rdy_en_valid, rdy_en_data = rdy_en.get_src_signals() # produce data
    rdy_buff_ready, rdy_buff_valid, rdy_buff_data = rdy_buff.get_src_signals() # produce data

    #--- Custom code begin ---#

    sl_vld, sl_vld_out = [Signal(bool(0)) for _ in range(2)] 
    hsd_en = Signal(bool(0))

    hsd_en_inst = mode.enable(rst, clk, inc_out_ready, sl_vld, hsd_en)

    delay_cnt = Signal(modbv(0, min=0, max=2**DELAY_BITS)) # should have full bit vector range
    count     = Signal(modbv(0, min=0, max=2**2))

    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_dly():
        if hsd_en:         
            delay_cnt.next = delay_cnt + 1 if mode_data == 0 else delay_cnt + 2


    @always_comb
    def vld_prcs():
        sl_vld_out.next = (delay_cnt == 0) and sl_vld


    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_cnt():
        if sl_vld_out:           
            count.next = count + 1


    @always_comb
    def out_prcs():
        rdy_en_data.next   = mode_valid
        rdy_buff_data.next = inc_out_ready
        inc_out_data.next  = count
        inc_out_valid.next = sl_vld_out

    #--- Custom code end   ---#

    return all_instances(rst, clk)
