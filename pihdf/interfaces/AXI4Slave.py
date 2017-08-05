from myhdl import *
from Bus   import Bus
from HSD   import HSD
from myhdl_lib import assign

class AXI4Slave(Bus):
    '''|
    | TODO
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2): # TODO bus_type to be removed

        self.DATA_WIDTH = 32
        self.ADDR_WIDTH = 32
        self.STRB_WIDTH = self.DATA_WIDTH/8

        axi_wd_fields = [("data"       , intbv(0)[self.DATA_WIDTH:]),
                         ("strobes"    , intbv(0)[self.STRB_WIDTH:])]

        axi_rd_fields = [("data"       , intbv(0)[self.DATA_WIDTH:]),
                         ("response"   , intbv(0)[2:])]

        axi4slave_ifs = lambda : [HSD(direction = 0, name = "waddr", data = self.ADDR_WIDTH),
                                  HSD(direction = 0, name = "wdata", data = axi_wd_fields),
                                  HSD(direction = 1, name = "wresp", data = 2),
                                  HSD(direction = 0, name = "raddr", data = self.ADDR_WIDTH),
                                  HSD(direction = 1, name = "rdata", data = axi_rd_fields)]

        # invoke base class constructor
        Bus.__init__(self, bus_type=axi4slave_ifs, name=name, reg_file=reg_file, filedump=filedump, lo=-3)

    def bus_logic_write(self, rst, clk):
        waddr = self.interface_list[0]
        wdata = self.interface_list[1]
        wresp = self.interface_list[2]
        waddr_rdy, waddr_vld, waddr_addr = waddr.get_snk_signals() # consume data
        wdata_rdy, wdata_vld, wdata_data, wdata_strb = wdata.get_snk_signals() # consume data
        wresp_rdy, wresp_vld, wresp_resp = wresp.get_src_signals() # produce data

        NUM_ADDR = len(self.ctrl.ls_addr)

        ls_we = [reg["we"] for reg in self.ctrl.ls]
        ls_wd = [reg["wd"] for reg in self.ctrl.ls]

        addr = Signal(intbv(0)[len(waddr_addr):])
        data = Signal(intbv(0)[len(wdata_data):])
        write_transaction = Signal(bool(0))

        ls_wd_data = [Signal(intbv(0)[self.DATA_WIDTH:]) for _ in range(NUM_ADDR)]
        asgn = [assign(ls_wd[i], ls_wd_data[i]) for i in range(NUM_ADDR)]

        @always_seq(clk.posedge, reset=rst)
        def write_regs():
            if write_transaction:
                write_transaction.next = 0
                waddr_rdy.next = 0
                wdata_rdy.next = 0
                wresp_vld.next = 0
            elif waddr_vld and wdata_vld:
                addr.next = waddr_addr
                data.next = wdata_data
                write_transaction.next = 1
                waddr_rdy.next = 1
                wdata_rdy.next = 1
                wresp_vld.next = 1
                wresp_resp.next = 0

        @always_comb
        def write_demux():
            for a in range(NUM_ADDR):
                ls_wd_data[a].next = data
                if (a == addr[:2]):
                    ls_we[a].next = write_transaction
                else:
                    ls_we[a].next = 0

        return instances()

    def bus_logic_read(self, rst, clk):
        raddr = self.interface_list[3]
        rdata = self.interface_list[4]
        raddr_rdy, raddr_vld, raddr_addr = raddr.get_snk_signals() # consume data
        rdata_rdy, rdata_vld, rdata_data, rdata_resp = rdata.get_src_signals() # produce data

        NUM_ADDR = len(self.ctrl.ls_addr)

        ls_re = [reg["re"] for reg in self.ctrl.ls]
        ls_rd = [reg["rd"] for reg in self.ctrl.ls]

        addr = Signal(intbv(0)[len(raddr_addr):])

        ls_rd_data = [Signal(intbv(0)[self.DATA_WIDTH:]) for _ in range(NUM_ADDR)]
        asgn = [assign(ls_rd_data[i], ls_rd[i]) for i in range(NUM_ADDR)]

        @always_seq(clk.posedge, reset=rst)
        def read_regs():
            if raddr_rdy:
                raddr_rdy.next = 0
            elif raddr_vld and not rdata_vld:
                addr.next = raddr_addr
                raddr_rdy.next = 1

            if rdata_vld and rdata_rdy:
                rdata_vld.next = 0
                for a in range(NUM_ADDR):
                    ls_re[a].next = 0
            elif raddr_rdy:
                rdata_vld.next = 1
                rdata_resp.next = 0
                rdata_data.next = 0xFFFFFFFF
                for a in range(NUM_ADDR):
                    if (a == addr[:2]):
                        ls_re[a].next = 1
                        rdata_data.next = ls_rd_data[a]
                    else:
                        ls_re[a].next = 0

        return instances()

    def create_rd_wr_logic(self, rst, clk, wd_if, ra, rd, ls, ls_addr, filename):
        x = self.bus_logic_write(rst, clk)
        y = self.bus_logic_read(rst, clk)
        return instances()

    def create_reg_file(self, rst, clk, filename=""):
        if self.reg_file:
            self.ctrl.create_address_map(self.DATA_WIDTH, filename)
            return self.create_rd_wr_logic(rst, clk, self.interface_list[0], self.interface_list[1], self.interface_list[2], self.ctrl.ls, self.ctrl.ls_addr, filename)
        else:
            return []


