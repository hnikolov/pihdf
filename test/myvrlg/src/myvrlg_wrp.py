from myhdl import *

def myvrlg_wrp(rst, clk, rx_hs, tx_hs, INST_NAME):

    """ Interface signals """
    rx_hs_ready,rx_hs_valid,rx_hs_data = rx_hs.get_snk_signals() # consume data
    tx_hs_ready,tx_hs_valid,tx_hs_data = tx_hs.get_src_signals() # produce data

    # Need this in order to work...
    @always(clk.posedge, rst)
    def pass_thru():
        pass

    #---------------------------------------------#
    # Define the interface to the verilog ip core #
    #---------------------------------------------#
    myvrlg_wrp.verilog_code = \
    """myvrlg $INST_NAME (\n""" + \
    """    .rst($rst),\n""" + \
    """    .clk($clk),\n""" + \
    """    .rx_hs_ready($rx_hs_ready),\n""" + \
    """    .rx_hs_valid($rx_hs_valid),\n""" + \
    """    .rx_hs_data($rx_hs_data),\n""" + \
    """    .tx_hs_ready($tx_hs_ready),\n""" + \
    """    .tx_hs_valid($tx_hs_valid),\n""" + \
    """    .tx_hs_data($tx_hs_data)\n""" + \
    """);"""

    #-------------------------------------------------------#
    # output, needed when converting the wrapper to verilog #
    #-------------------------------------------------------#
    rx_hs_ready.driven = "wire"
    tx_hs_valid.driven = "wire"
    tx_hs_data.driven = "wire"
    
    return pass_thru


