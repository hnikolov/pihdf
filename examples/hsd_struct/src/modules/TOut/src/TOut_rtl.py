from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def TOut_rtl(rst, clk, mode, inc_in, LEDs, rdy_out):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    mode_ready, mode_valid, mode_data = mode.get_snk_signals() # consume data
    inc_in_ready, inc_in_valid, inc_in_data = inc_in.get_snk_signals() # consume data
    LEDs_ready, LEDs_valid, LEDs_data = LEDs.get_src_signals() # produce data
    rdy_out_ready, rdy_out_valid, rdy_out_data = rdy_out.get_src_signals() # produce data

    #--- Custom code begin ---#

    mode_data_r   = Signal(intbv(0)   [2:])
    default_out_r = Signal(intbv(0x15)[5:])
    hsd_en        = Signal(bool(0))

    hsd_en_inst   = inc_in.enable(rst, clk, LEDs_ready, LEDs_valid, hsd_en)

    @always_seq(clk.posedge, reset=rst)
    def prcs_mode_data_r():
        if mode_valid == 1:
            mode_data_r.next = mode_data


    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_hs():
        if hsd_en:           
            if mode_data_r == 0:
                LEDs_data.next[2:0] = inc_in_data[2:0]
                LEDs_data.next[4:2] = inc_in_data[2:0]
                LEDs_data.next[4]   = 0
            
            elif mode_data_r == 1:
                if   inc_in_data == 0: LEDs_data.next = 1
                elif inc_in_data == 1: LEDs_data.next = 2
                elif inc_in_data == 2: LEDs_data.next = 4
                elif inc_in_data == 3: LEDs_data.next = 8

            elif mode_data_r == 2:
                if   inc_in_data == 0: LEDs_data.next = 8
                elif inc_in_data == 1: LEDs_data.next = 4
                elif inc_in_data == 2: LEDs_data.next = 2
                elif inc_in_data == 3: LEDs_data.next = 1

            else:
                LEDs_data.next = default_out_r


    @always_comb
    def out_prcs():
        rdy_out_data.next = LEDs_ready


    #--- Custom code end   ---#

    return all_instances(rst, clk)
