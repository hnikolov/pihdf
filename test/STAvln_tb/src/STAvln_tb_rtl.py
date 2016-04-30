from myhdl import *
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def STAvln_tb_rtl(rst, clk, rx16, tx16, rx32, tx32, rx64, tx64, ipg_rx16, ipg_tx16):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    rx16_ready, rx16_valid, rx16_sop, rx16_eop, rx16_empty, rx16_data, rx16_err = rx16.get_snk_signals() # consume data
    tx16_ready, tx16_valid, tx16_sop, tx16_eop, tx16_empty, tx16_data, tx16_err = tx16.get_src_signals() # produce data
    rx32_ready, rx32_valid, rx32_sop, rx32_eop, rx32_empty, rx32_data, rx32_err = rx32.get_snk_signals() # consume data
    tx32_ready, tx32_valid, tx32_sop, tx32_eop, tx32_empty, tx32_data, tx32_err = tx32.get_src_signals() # produce data
    rx64_ready, rx64_valid, rx64_sop, rx64_eop, rx64_empty, rx64_data, rx64_err = rx64.get_snk_signals() # consume data
    tx64_ready, tx64_valid, tx64_sop, tx64_eop, tx64_empty, tx64_data, tx64_err = tx64.get_src_signals() # produce data
    ipg_rx16_ready, ipg_rx16_valid, ipg_rx16_data = ipg_rx16.get_src_signals() # produce data
    ipg_tx16_ready, ipg_tx16_valid, ipg_tx16_data = ipg_tx16.get_src_signals() # produce data

    #--- Custom code begin ---#
    """
    =============================================
    = rx -> REG -> tx
    =============================================
    """
    NUM_STAGES      = 1

    stage16_en      = Signal(intbv(0)[NUM_STAGES:])
    stage32_en      = Signal(intbv(0)[NUM_STAGES:])
    stage64_en      = Signal(intbv(0)[NUM_STAGES:])

    pipe_ctrl16_i   = pipeline_control( rst             = rst,
                                        clk             = clk,
                                        rx_vld          = rx16_valid,
                                        rx_rdy          = rx16_ready,
                                        tx_vld          = tx16_valid,
                                        tx_rdy          = tx16_ready,
                                        stage_enable    = stage16_en)

    pipe_ctrl32_i   = pipeline_control( rst             = rst,
                                        clk             = clk,
                                        rx_vld          = rx32_valid,
                                        rx_rdy          = rx32_ready,
                                        tx_vld          = tx32_valid,
                                        tx_rdy          = tx32_ready,
                                        stage_enable    = stage32_en)

    pipe_ctrl64_i   = pipeline_control( rst             = rst,
                                        clk             = clk,
                                        rx_vld          = rx64_valid,
                                        rx_rdy          = rx64_ready,
                                        tx_vld          = tx64_valid,
                                        tx_rdy          = tx64_ready,
                                        stage_enable    = stage64_en)

    @always_seq(clk.posedge, rst)
    def reg_proc():
        if (stage16_en[0]):
            tx16_sop.next   = rx16_sop
            tx16_eop.next   = rx16_eop
            tx16_empty.next = rx16_empty
            tx16_data.next  = rx16_data
            tx16_err.next   = rx16_err

        if (stage32_en[0]):
            tx32_sop.next   = rx32_sop
            tx32_eop.next   = rx32_eop
            tx32_empty.next = rx32_empty
            tx32_data.next  = rx32_data
            tx32_err.next   = rx32_err

        if (stage64_en[0]):
            tx64_sop.next   = rx64_sop
            tx64_eop.next   = rx64_eop
            tx64_empty.next = rx64_empty
            tx64_data.next  = rx64_data
            tx64_err.next   = rx64_err

    """
    =============================================
    = Measure IPG for rx16
    =============================================
    """
    ipg_rx16_cnt  = Signal(intbv(0)[len(ipg_rx16_data):])
    ipg_rx16_en   = Signal(bool(0))

    @always(clk.posedge)
    def ipg_rx16_proc():
        if (rst):
            ipg_rx16_cnt.next    = 0
            ipg_rx16_valid.next  = 0
            ipg_rx16_en.next     = 0
        else:
            if (ipg_rx16_en):
                # Count and report the IPGs
                ipg_rx16_valid.next  = 0
                if (not rx16_valid):
                    ipg_rx16_cnt.next    = ipg_rx16_cnt + 1
                elif (rx16_ready):
                    if (rx16_sop):
                        ipg_rx16_cnt.next    = 0
                        ipg_rx16_data.next   = ipg_rx16_cnt
                        ipg_rx16_valid.next  = 1
                    elif(rx16_eop):
                        ipg_rx16_cnt.next    = 0
            else:
                # Wait for the first transaction and start the IPG counting
                if (rx16_valid and rx16_ready and rx16_eop):
                    ipg_rx16_en.next = 1

    """
    =============================================
    = Measure IPG for tx16
    =============================================
    """
    ipg_tx16_cnt    = Signal(intbv(0)[len(ipg_tx16_data):])
    ipg_tx16_en     = Signal(bool(0))

    @always(clk.posedge)
    def ipg_tx16_proc():
        if (rst):
            ipg_tx16_cnt.next    = 0
            ipg_tx16_valid.next  = 0
        else:
            if (ipg_tx16_en):
                # Count and report the IPGs
                ipg_tx16_valid.next  = 0
                if (not tx16_ready):
                    ipg_tx16_cnt.next    = ipg_tx16_cnt + 1
                elif (tx16_valid):
                    if (tx16_sop):
                        ipg_tx16_cnt.next    = 0
                        ipg_tx16_data.next   = ipg_tx16_cnt
                        ipg_tx16_valid.next  = 1
                    elif (tx16_eop):
                        ipg_tx16_cnt.next    = 0
            else:
                # Wait for the first transaction and start the IPG counting
                if (tx16_valid and tx16_ready and tx16_eop):
                    ipg_tx16_en.next = 1

    #--- Custom code end   ---#

    return all_instances(rst, clk)
