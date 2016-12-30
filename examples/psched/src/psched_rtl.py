from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def psched_rtl(rst, clk, rx_port, tx_port, sequence, rx, tx):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    rx_port_ready, rx_port_valid, rx_port_cmd, rx_port_port = rx_port.get_snk_signals() # consume data
    tx_port_ready, tx_port_valid, tx_port_cmd, tx_port_port = tx_port.get_src_signals() # produce data
    sequence_ready, sequence_valid, sequence_data = sequence.get_src_signals() # produce data
    rx_ready, rx_valid, rx_sop, rx_eop, rx_empty, rx_data, rx_err = rx.get_snk_signals() # consume data
    tx_ready, tx_valid, tx_sop, tx_eop, tx_empty, tx_data, tx_err = tx.get_src_signals() # produce data

    #--- Custom code begin ---#
    port_en, st_en = [Signal(bool(0)) for i in range(2)]

    port_en_inst = rx_port.enable(rst, clk, tx_port_ready, tx_port_valid, port_en)
    st_en_inst = rx.enable(rst, clk, tx_ready, tx_valid, st_en)


    # Port fields interface
    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_port_flds():
        if port_en:
            tx_port_cmd.next  = rx_port_cmd
            tx_port_port.next = rx_port_port

            
    # STAvln
    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_st():
        if st_en:
            tx_sop.next   = rx_sop
            tx_eop.next   = rx_eop
            tx_empty.next = rx_empty
            tx_data.next  = rx_data
            tx_err.next   = rx_err

    #--- Custom code end   ---#

    return all_instances(rst, clk)
