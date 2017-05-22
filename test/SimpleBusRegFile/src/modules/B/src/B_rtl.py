from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
from A.A import A
#--- Custom code end   ---#

def B_rtl(rst, clk, sbus):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    sbus_wa_wd, sbus_raddr, sbus_rdata = sbus.interfaces()
    sbus_wa_wd_ready, sbus_wa_wd_valid, sbus_wa_wd_addr, sbus_wa_wd_data = sbus_wa_wd.get_snk_signals() # consume data
    sbus_raddr_ready, sbus_raddr_valid, sbus_raddr_data = sbus_raddr.get_snk_signals() # consume data
    sbus_rdata_ready, sbus_rdata_valid, sbus_rdata_data = sbus_rdata.get_src_signals() # produce data

    #--- Custom code begin ---#
    RTL = 1

    # Instance that uses ctrl
    A1 = A(RTL).gen(rst=rst, clk=clk, sbus=sbus)


    # Local usage of ctrl
    re, rdata, we, wdata = sbus.ctrl.get_interface('rw', 4*8, 'reg')

    c = Signal(modbv(0)[4*8:])

    @always_seq(clk.posedge, reset=rst)
    def my_c():
        if we:
            c.next = wdata

    @always_comb
    def comb():
        rdata.next = c if re == 1 else 0

    we_1, wdata_1 = sbus.ctrl.get_interface('wo', 4*8, 'w_reg')
    re_1, rdata_1 = sbus.ctrl.get_interface('ro', 4*8, 'r_reg')

#    wreg = Signal(modbv(0)[4*8:])
    
    wreg = HSD(data=4*8, buf_size=8)
    
    wreg_w_rdy, wreg_w_vld, wreg_w_data = wreg.get_src_signals() 
    wreg_r_rdy, wreg_r_vld, wreg_r_data = wreg.get_snk_signals() 
    
    @always_comb
    def assign_data():
        wreg_w_vld.next  = we_1
        wreg_w_data.next = wdata_1
        wreg_r_rdy.next  = re_1
        rdata_1.next     = wreg_r_data

#    @always_seq(clk.posedge, reset=rst)
#    def my_wreg():
#        if we_1:
#            wreg.next = wdata_1
#
#    @always_comb
#    def comb_1():
#        rdata_1.next = wreg if re_1 == 1 else 0


    #--- Custom code end   ---#

    return all_instances(rst, clk)
