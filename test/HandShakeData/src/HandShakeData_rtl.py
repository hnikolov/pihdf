from myhdl import *
import pihdf
from pihdf import *
from myhdl_lib import *

from modules.submodule_rx.submodule_rx import submodule_rx
from modules.submodule_tx.submodule_tx import submodule_tx

#--- Custom code begin ---#
#--- Custom code end   ---#

def HandShakeData_rtl(rst, clk, rx_width, tx_width, rx_width1, tx_width1, rx_fields, tx_fields, rx_width_buf, tx_width_buf, rx_width1_buf, tx_width1_buf, rx_fields_buf, tx_fields_buf, rx_fields_const, tx_fields_const, rx_push, tx_pull, rx_terminate, tx_terminate, ipg_rx_width, ipg_tx_width, IMPL, FDUMP):
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
    rx_fields_const_ready, rx_fields_const_valid, rx_fields_const_bit, rx_fields_const_byte, rx_fields_const_word = rx_fields_const.get_snk_signals() # consume data
    tx_fields_const_ready, tx_fields_const_valid, tx_fields_const_bit, tx_fields_const_byte, tx_fields_const_word = tx_fields_const.get_src_signals() # produce data
    rx_push_ready, rx_push_valid, rx_push_data = rx_push.get_snk_signals() # consume data
    tx_pull_ready, tx_pull_valid, tx_pull_data = tx_pull.get_src_signals() # produce data
    rx_terminate_ready, rx_terminate_valid, rx_terminate_data = rx_terminate.get_snk_signals() # consume data
    tx_terminate_ready, tx_terminate_valid, tx_terminate_data = tx_terminate.get_src_signals() # produce data
    ipg_rx_width_ready, ipg_rx_width_valid, ipg_rx_width_data = ipg_rx_width.get_src_signals() # produce data
    ipg_tx_width_ready, ipg_tx_width_valid, ipg_tx_width_data = ipg_tx_width.get_src_signals() # produce data

    """ Local interfaces """
    hs_width = HSD(data=64, filedump=FDUMP)
    hs_width1 = HSD(data=1, filedump=FDUMP)
    hs_fields = HSD(data=test_fields, filedump=FDUMP)
    hs_width_buf = HSD(data=64, buf_size=4, filedump=FDUMP)
    hs_width1_buf = HSD(data=1, buf_size=4, filedump=FDUMP)
    hs_fields_buf = HSD(data=test_fields, buf_size=4, filedump=FDUMP)
    hs_terminate_snk = HSD(data=64, terminate=True, filedump=FDUMP)
    hs_terminate_src = HSD(data=64, terminate=True, filedump=FDUMP)

    if isinstance(IMPL, dict):
        my_submodule_rx_impl = IMPL["my_submodule_rx"] if "my_submodule_rx" in IMPL else IMPL["top"]
        my_submodule_tx_impl = IMPL["my_submodule_tx"] if "my_submodule_tx" in IMPL else IMPL["top"]
    else:
        my_submodule_rx_impl = IMPL
        my_submodule_tx_impl = IMPL

    """ Components """
    my_submodule_rx = submodule_rx(my_submodule_rx_impl).gen(rx_width=rx_width, tx_width=hs_width, ipg_rx_width=ipg_rx_width, clk=clk, rx_width1=rx_width1, tx_fields_buf=hs_fields_buf, tx_width1_buf=hs_width1_buf, tx_fields=hs_fields, tx_width1=hs_width1, tx_terminate=hs_terminate_snk, rx_fields_buf=rx_fields_buf, rx_terminate=rx_terminate, rx_width1_buf=rx_width1_buf, rst=rst, rx_fields=rx_fields, rx_push=rx_push, rx_width_buf=rx_width_buf, tx_width_buf=hs_width_buf)
    my_submodule_tx = submodule_tx(my_submodule_tx_impl).gen(rx_width=hs_width, tx_width=tx_width, clk=clk, rx_width1=hs_width1, tx_fields_buf=tx_fields_buf, tx_width1_buf=tx_width1_buf, tx_fields=tx_fields, tx_width1=tx_width1, tx_terminate=tx_terminate, rx_fields_buf=hs_fields_buf, rx_terminate=hs_terminate_src, rx_width1_buf=hs_width1_buf, rst=rst, rx_fields=hs_fields, rx_fields_const=rx_fields_const, ipg_tx_width=ipg_tx_width, rx_width_buf=hs_width_buf, tx_pull=tx_pull, tx_fields_const=tx_fields_const, tx_width_buf=tx_width_buf)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
