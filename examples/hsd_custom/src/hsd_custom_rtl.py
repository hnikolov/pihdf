from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def hsd_custom_rtl(rst, clk, rx_port_flds, tx_port_flds):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    rx_port_flds_ready, rx_port_flds_valid, rx_port_flds_cmd, rx_port_flds_port = rx_port_flds.get_snk_signals() # consume data
    tx_port_flds_ready, tx_port_flds_valid, tx_port_flds_cmd, tx_port_flds_port = tx_port_flds.get_src_signals() # produce data

    #--- Custom code begin ---#
    hs_en, avln_en, flds_en = [Signal(bool(0)) for i in range(3)]

    flds_en_inst = rx_port_flds.enable(rst, clk, tx_port_flds_ready, tx_port_flds_valid, flds_en)

    # Port fields interface
    @always_seq(clk.posedge, reset=rst)
    def clk_prcs_port_flds():        
        if flds_en:
            tx_port_flds_cmd.next   = rx_port_flds_cmd
            tx_port_flds_port.next  = rx_port_flds_port
            
    #--- Custom code end   ---#

    return all_instances(rst, clk)
