from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def A_rtl(rst, clk, sbus):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    sbus_wa_wd, sbus_raddr, sbus_rdata = sbus.interfaces()
    sbus_wa_wd_ready, sbus_wa_wd_valid, sbus_wa_wd_addr, sbus_wa_wd_data = sbus_wa_wd.get_snk_signals() # consume data
    sbus_raddr_ready, sbus_raddr_valid, sbus_raddr_data = sbus_raddr.get_snk_signals() # consume data
    sbus_rdata_ready, sbus_rdata_valid, sbus_rdata_data = sbus_rdata.get_src_signals() # produce data

    #--- Custom code begin ---#
    reg_file = sbus.ctrl
    
    re, rdata, we, wdata = reg_file.get_interface("rw", 4*8, 'register')
    my_reg = Signal(modbv(0)[4*8:])

    @always_seq(clk.posedge, reset=rst)
    def reg_prcs():
        if we:
            my_reg.next = wdata

    @always_comb
    def comb():
        rdata.next = my_reg


        
    we_1, wdata_1 = reg_file.get_interface("wg", 4*8, 'glob_reg')
    g_reg = Signal(modbv(0)[4*8:])

    @always_seq(clk.posedge, reset=rst)
    def g_reg_prcs():
        if we_1:
            g_reg.next = wdata_1


    small = 3*8
    re_2, rdata_2, we_2, wdata_2 = reg_file.get_interface("rw", small, 'small_reg')
    my_small_reg = Signal(intbv(0)[small:])

    @always_seq(clk.posedge, reset=rst)
    def reg_prcs23():
        if we_2:
            my_small_reg.next = wdata_2

    @always_comb
    def comb23():
        rdata_2.next = my_small_reg

    #--- Custom code end   ---#

    return all_instances(rst, clk)
