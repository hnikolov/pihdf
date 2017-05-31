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

    my_b_reg = Signal(modbv(0)[4*8:])

    @always_seq(clk.posedge, reset=rst)
    def prcs_my_b_reg():
        if we:
            my_b_reg.next = wdata

    @always_comb
    def comb():
        rdata.next = my_b_reg if re == 1 else 0

    we_1, wdata_1 = sbus.ctrl.get_interface('wo', 4*8, 'w_reg')
    re_1, rdata_1 = sbus.ctrl.get_interface('ro', 4*8, 'r_reg')

    # Connect a FIFO to the SimpleBus --------------------------
    fifo = HSD(data=4*8, buf_size=4)
    
    fifo_w_rdy, fifo_w_vld, fifo_w_data = fifo.get_src_signals()
    fifo_r_rdy, fifo_r_vld, fifo_r_data = fifo.get_snk_signals()
    
    # Writes and reads are not blocking.
    # To get the FIFO status, we need to map emty and full to another address/register
    @always_comb
    def assign_data():
        fifo_w_vld.next  = we_1
        fifo_w_data.next = wdata_1
        fifo_r_rdy.next  = re_1
        rdata_1.next     = fifo_r_data

    #--- Custom code end   ---#

    return all_instances(rst, clk)
