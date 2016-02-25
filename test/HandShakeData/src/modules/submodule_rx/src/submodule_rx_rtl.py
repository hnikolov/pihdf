from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

#--- Custom code begin ---#
#--- Custom code end   ---#

def submodule_rx_rtl(rst, clk, rx_width, tx_width, rx_width1, tx_width1, rx_fields, tx_fields, rx_width_buf, tx_width_buf, rx_width1_buf, tx_width1_buf, rx_fields_buf, tx_fields_buf, rx_push, rx_terminate, tx_terminate, ipg_rx_width):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    rx_width_ready, rx_width_valid, rx_width_data = rx_width.get_snk_signals() # consume data
    tx_width_ready, tx_width_valid, tx_width_data = tx_width.get_src_signals() # produce data
    rx_width1_ready, rx_width1_valid, rx_width1_data = rx_width1.get_snk_signals() # consume data
    tx_width1_ready, tx_width1_valid, tx_width1_data = tx_width1.get_src_signals() # produce data
    rx_fields_ready, rx_fields_valid, rx_fields_bit, rx_fields_byte, rx_fields_word = rx_fields.get_snk_signals() # consume data
    tx_fields_ready, tx_fields_valid, tx_fields_bit, tx_fields_byte, tx_fields_word = tx_fields.get_src_signals() # produce data
    rx_width_buf_ready, rx_width_buf_valid, rx_width_buf_data = rx_width_buf.get_snk_signals() # consume data
    tx_width_buf_ready, tx_width_buf_valid, tx_width_buf_data = tx_width_buf.get_src_signals() # produce data
    rx_width1_buf_ready, rx_width1_buf_valid, rx_width1_buf_data = rx_width1_buf.get_snk_signals() # consume data
    tx_width1_buf_ready, tx_width1_buf_valid, tx_width1_buf_data = tx_width1_buf.get_src_signals() # produce data
    rx_fields_buf_ready, rx_fields_buf_valid, rx_fields_buf_bit, rx_fields_buf_byte, rx_fields_buf_word = rx_fields_buf.get_snk_signals() # consume data
    tx_fields_buf_ready, tx_fields_buf_valid, tx_fields_buf_bit, tx_fields_buf_byte, tx_fields_buf_word = tx_fields_buf.get_src_signals() # produce data
    rx_push_ready, rx_push_valid, rx_push_data = rx_push.get_snk_signals() # consume data
    rx_terminate_ready, rx_terminate_valid, rx_terminate_data = rx_terminate.get_snk_signals() # consume data
    tx_terminate_ready, tx_terminate_valid, tx_terminate_data = tx_terminate.get_src_signals() # produce data
    ipg_rx_width_ready, ipg_rx_width_valid, ipg_rx_width_data = ipg_rx_width.get_src_signals() # produce data

    #--- Custom code begin ---#
    """
    =============================================
    = rx_width pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_width_en        = Signal(intbv(0)[NUM_STAGES:])

    rx_width_pipe      = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_width_valid,
                                           rx_rdy          = rx_width_ready,
                                           tx_vld          = tx_width_valid,
                                           tx_rdy          = tx_width_ready,
                                           stage_enable    = rx_width_en)
    @always_seq(clk.posedge, rst)
    def rx_width_pipe_proc():
        if (rx_width_en[0]):
            tx_width_data.next = rx_width_data

    """
    =============================================
    = rx_width1 pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_width1_en        = Signal(intbv(0)[NUM_STAGES:])

    rx_width1_pipe      = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_width1_valid,
                                           rx_rdy          = rx_width1_ready,
                                           tx_vld          = tx_width1_valid,
                                           tx_rdy          = tx_width1_ready,
                                           stage_enable    = rx_width1_en)
    @always_seq(clk.posedge, rst)
    def rx_width1_pipe_proc():
        if (rx_width1_en[0]):
            tx_width1_data.next = rx_width1_data

    """
    =============================================
    = rx_fields pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_fields_en       = Signal(intbv(0)[NUM_STAGES:])

    rx_fields_pipe     = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_fields_valid,
                                           rx_rdy          = rx_fields_ready,
                                           tx_vld          = tx_fields_valid,
                                           tx_rdy          = tx_fields_ready,
                                           stage_enable    = rx_fields_en)

    @always_seq(clk.posedge, rst)
    def rx_fields_proc():
        if (rx_fields_en[0]):
            tx_fields_bit.next  = rx_fields_bit
            tx_fields_byte.next = rx_fields_byte
            tx_fields_word.next = rx_fields_word

    """
    =============================================
    = rx_width_buf pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_width_buf_en    = Signal(intbv(0)[NUM_STAGES:])

    rx_width_buf_pipe  = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_width_buf_valid,
                                           rx_rdy          = rx_width_buf_ready,
                                           tx_vld          = tx_width_buf_valid,
                                           tx_rdy          = tx_width_buf_ready,
                                           stage_enable    = rx_width_buf_en)
    @always_seq(clk.posedge, rst)
    def rx_width_buf_pipe_proc():
        if (rx_width_buf_en[0]):
            tx_width_buf_data.next = rx_width_buf_data

    """
    =============================================
    = rx_width1_buf pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_width1_buf_en    = Signal(intbv(0)[NUM_STAGES:])

    rx_width1_buf_pipe  = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_width1_buf_valid,
                                           rx_rdy          = rx_width1_buf_ready,
                                           tx_vld          = tx_width1_buf_valid,
                                           tx_rdy          = tx_width1_buf_ready,
                                           stage_enable    = rx_width1_buf_en)
    @always_seq(clk.posedge, rst)
    def rx_width1_buf_pipe_proc():
        if (rx_width1_buf_en[0]):
            tx_width1_buf_data.next = rx_width1_buf_data

    """
    =============================================
    = rx_fields_buf pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_fields_buf_en   = Signal(intbv(0)[NUM_STAGES:])

    rx_fields_buf_pipe = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_fields_buf_valid,
                                           rx_rdy          = rx_fields_buf_ready,
                                           tx_vld          = tx_fields_buf_valid,
                                           tx_rdy          = tx_fields_buf_ready,
                                           stage_enable    = rx_fields_buf_en)

    @always_seq(clk.posedge, rst)
    def rx_fields_buf_proc():
        if (rx_fields_buf_en[0]):
            tx_fields_buf_bit.next  = rx_fields_buf_bit
            tx_fields_buf_byte.next = rx_fields_buf_byte
            tx_fields_buf_word.next = rx_fields_buf_word

    """
    =============================================
    = rx_terminate pass through pipeline
    =============================================
    """
    NUM_STAGES      = 1

    rx_terminate_en    = Signal(intbv(0)[NUM_STAGES:])

    rx_terminate_pipe  = pipeline_control( rst             = rst,
                                           clk             = clk,
                                           rx_vld          = rx_terminate_valid,
                                           rx_rdy          = rx_terminate_ready,
                                           tx_vld          = tx_terminate_valid,
                                           tx_rdy          = tx_terminate_ready,
                                           stage_enable    = rx_terminate_en)
    @always_seq(clk.posedge, rst)
    def rx_terminate_pipe_proc():
        if (rx_terminate_en[0]):
            tx_terminate_data.next = rx_terminate_data

    """
    =============================================
    = rx_push 
    =============================================
    """
    # rx_push_ready signal should not be driven by the receiver, because this interface is declared as a PUSH interface

    @always_seq(clk.posedge, rst)
    def rx_push_proc():
        if (rx_push_valid):
            assert rx_push_data == 0x55, "rx_push interface receives unexpected data , expected 0x55"

    """
    =============================================
    = Measure IPG for rx_width
    =============================================
    """
    ipg_rx_width_cnt     = Signal(intbv(0)[len(ipg_rx_width_data):])
    ipg_rx_width_en      = Signal(bool(0))

    @always(clk.posedge)
    def ipg_rxx_proc():
        if (rst):
            ipg_rx_width_cnt.next    = 0
            ipg_rx_width_data.next   = 0
            ipg_rx_width_valid.next  = 0
            ipg_rx_width_en.next     = 0
        else:
            if (ipg_rx_width_en):
                # Count and report the IPGs
                ipg_rx_width_valid.next  = 0
                if (not rx_width_valid):
                    ipg_rx_width_cnt.next    = ipg_rx_width_cnt + 1
                elif (rx_width_ready):
                    ipg_rx_width_cnt.next    = 0
                    ipg_rx_width_data.next   = ipg_rx_width_cnt
                    ipg_rx_width_valid.next  = 1
            else:
                # Wait for the first transaction and start the IPG counting
                if (rx_width_valid and rx_width_ready):
                    ipg_rx_width_en.next = 1



    #--- Custom code end   ---#

    return all_instances(rst, clk)
