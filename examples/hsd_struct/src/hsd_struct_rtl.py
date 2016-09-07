from myhdl import *
from pihdf import *
from myhdl_lib import *

from modules.TIncr.TIncr import TIncr
from modules.TOut.TOut import TOut

#--- Custom code begin ---#
#--- Custom code end   ---#

def hsd_struct_rtl(rst, clk, mode_1, mode_2, LEDs, LED_rdy_en, LED_rdy_buff, LED_rdy_out, DELAY_BITS, BUFFER_SIZE, IMPL, FDUMP):
    '''|
    | Top-level MyHDL description. This is converted to RTL velilog...
    |________'''

    """ Interface signals """
    mode_1_ready, mode_1_valid, mode_1_data = mode_1.get_snk_signals() # consume data
    mode_2_ready, mode_2_valid, mode_2_data = mode_2.get_snk_signals() # consume data
    LEDs_ready, LEDs_valid, LEDs_data = LEDs.get_src_signals() # produce data
    LED_rdy_en_ready, LED_rdy_en_valid, LED_rdy_en_data = LED_rdy_en.get_src_signals() # produce data
    LED_rdy_buff_ready, LED_rdy_buff_valid, LED_rdy_buff_data = LED_rdy_buff.get_src_signals() # produce data
    LED_rdy_out_ready, LED_rdy_out_valid, LED_rdy_out_data = LED_rdy_out.get_src_signals() # produce data

    """ Local interfaces """
    buff = HSD(data=2, buf_size=18, filedump=FDUMP)

    if isinstance(IMPL, dict):
        mIncr_impl = IMPL["mIncr"] if "mIncr" in IMPL else IMPL["top"]
        mOut_impl = IMPL["mOut"] if "mOut" in IMPL else IMPL["top"]
    else:
        mIncr_impl = IMPL
        mOut_impl = IMPL

    """ Components """
    mIncr = TIncr(mIncr_impl).gen(clk=clk, inc_out=buff, rdy_en=LED_rdy_en, DELAY_BITS=DELAY_BITS, mode=mode_1, rdy_buff=LED_rdy_buff, rst=rst)
    mOut = TOut(mOut_impl).gen(inc_in=buff, LEDs=LEDs, clk=clk, rdy_out=LED_rdy_out, mode=mode_2, rst=rst)

    #--- Custom code begin ---#
    #--- Custom code end   ---#

    return all_instances(rst, clk)
