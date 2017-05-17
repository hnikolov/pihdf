from myhdl import *
from Bus   import Bus
from HSD   import HSD

import math 
from myhdl_lib import pipeline_control, assign


class SimpleBus(Bus):
    '''|
    | TODO
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2): # TODO bus_type to be removed

        self.BUS_DWIDTH = 32

        wd_fields = [("addr", intbv(0)[8:]),
                     ("data", intbv(0)[self.BUS_DWIDTH:])]

        sbus_ifs = lambda : [ HSD(direction = 0, name = "wa_wd", data = wd_fields),
                              HSD(direction = 0, name = "raddr", data = 8),
                              HSD(direction = 1, name = "rdata", data = self.BUS_DWIDTH) ]

        # Invoke base class constructor
        Bus.__init__(self, bus_type=sbus_ifs, name=name, reg_file=reg_file, filedump=filedump, lo=-3)

# ----------------------------------------------------------------------------------------------------------------
    def create_rd_wr_logic(self, rst, clk, wd_if, ra, rd, ls, ls_addr, filename):
        '''|
        | Creates a reg file from all interfaces stored in ls
        |________'''

        wr_rdy, wr_vld, wr_addr, wr_data = wd_if.get_snk_signals() # consume data
        ra_rdy, ra_vld, ra_data = ra.get_snk_signals() # consume data
        rd_rdy, rd_vld, rd_data = rd.get_src_signals() # produce data

        ls_we = []
        ls_wd = []
        ls_re = []
        ls_rd = []

        for i in ls:
            assert (i["width"] <= self.BUS_DWIDTH), "Register {} width {:} bit exceeds the bus width {:} bit".format(i["iname"], i["width"], self.BUS_DWIDTH)
            ls_re.append(i["re"])
            ls_rd.append(i["rd"])
            ls_we.append(i["we"])
            ls_wd.append(i["wd"])

        NUM_ADDR = len(ls_addr)

        def bus_logic_write(rst, clk, wr_rdy, wr_vld, wr_addr, wr_data, ls_we, ls_wd):
            '''|
            | Creates a reg file from all interfaces stored in ls
            |________'''

            ls_wd_data = [Signal(intbv(0)[self.BUS_DWIDTH:]) for _ in range(NUM_ADDR)]
            asgn = [assign(ls_wd[i], ls_wd_data[i]) for i in range(NUM_ADDR)]

            @always_comb
            def we_demux():
                wr_rdy.next = 1
                for a in range(NUM_ADDR):
                    ls_we[a].next      = 0
                    ls_wd_data[a].next = 0

                    if (a == wr_addr):
                        ls_we[a].next      = wr_vld
                        ls_wd_data[a].next = wr_data

            return instances()

        bwrite = bus_logic_write(rst, clk, wr_rdy, wr_vld, wr_addr, wr_data, ls_we, ls_wd)


        def bus_logic_read(rst, clk, ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data, ls_re, ls_rd):
            '''|
            | Creates a reg file from all interfaces stored in ls
            |________'''

            ls_rd_data = [Signal(intbv(0)[self.BUS_DWIDTH:]) for _ in range(NUM_ADDR)]
            asgn = [assign(ls_rd_data[i], ls_rd[i]) for i in range(NUM_ADDR)]

#            @always_seq(clk.posedge, reset=rst)
            @always_comb
            def logic_rd():
                ra_rdy.next  = 1          # Simple Bus -> ready/valid not used
                rd_vld.next  = ra_vld     # but not used (Simple Bus)
                rd_data.next = 0xffffffff # To recognize not valid data

                if( ra_vld == 1 ):
                    for a in range(NUM_ADDR):
                        ls_re[a].next = 0
                        if( a == ra_data ):
                            ls_re[a].next = 1
                            rd_data.next  = ls_rd_data[a]

            return instances()

        bread = bus_logic_read(rst, clk, ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data, ls_re, ls_rd)

        return instances()

    
# ----------------------------------------------------------------------------------------------------------------
    def create_reg_file(self, rst, clk, filename=""):
        '''|
        | The class API/Interface. Overrides the base Bus method.
        |________'''
        if self.reg_file:
            self.ctrl.create_address_map(self.BUS_DWIDTH, filename)
            return self.create_rd_wr_logic(rst, clk, self.interface_list[0], self.interface_list[1], self.interface_list[2], self.ctrl.ls, self.ctrl.ls_addr, filename)
        else:
            return []
