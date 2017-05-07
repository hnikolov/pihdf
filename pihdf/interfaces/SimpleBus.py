from myhdl import *
from Bus   import Bus
from HSD   import HSD

# TODO: temp
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

        self.ctrl.print_register_list(filename)

        wr_rdy, wr_vld, wr_addr, wr_data = wd_if.get_snk_signals() # consume data
        ra_rdy, ra_vld, ra_data = ra.get_snk_signals() # consume data
        rd_rdy, rd_vld, rd_data = rd.get_src_signals() # produce data

        ls_we = []
        ls_wd = []
        ls_re = []
        ls_rd = []

        for i in ls:
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
                    if (a == wr_addr):
                        ls_we[a].next = wr_vld
                        ls_wd_data[a].next = wr_data
                    else:
                        ls_we[a].next = 0
                        ls_wd_data[a].next = 0xff

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
                ra_rdy.next = 1 # Simple Bus -> ready/valid not used
                rd_vld.next  = ra_vld
                rd_data.next = 0xffffffff

                if( ra_vld == 1 ):
                    for a in range(NUM_ADDR):
                        ls_re[a].next = 0
                        if( a == ra_data ):
                            ls_re[a].next = 1 # Do we need this?
                            rd_data.next = ls_rd_data[a]

            return instances()

        bread = bus_logic_read(rst, clk, ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data, ls_re, ls_rd)

        return instances()


    #--------------------------------------------------------------------------------------------------------------
    def create_rd_wr_logic_orig(self, rst, clk, wd_if, ra, rd, ls, ls_addr, filename):
        '''|
        | Creates a reg file from all interfaces stored in ls
        |________'''    

        self.ctrl.print_register_list(filename)
        
        wr_rdy, wr_vld, wr_addr, wr_data = wd_if.get_snk_signals() # consume data
        rd_rdy, rd_vld, rd_data = rd.get_src_signals() # produce data
        ra_rdy, ra_vld, ra_data = ra.get_snk_signals() # consume data

        ls_we = []
        ls_wd = []
        ls_re = []
        ls_rd = []

        for i in ls:
            ls_re.append(i["re"])
            ls_rd.append(i["rd"])
            ls_we.append(i["we"])
            ls_wd.append(i["wd"])

        WBUS_WIDTH = len(wr_data)
        NUM_REGS   = len(ls)
    
        # Deser registers
        NUM_ADDR = sum([len(ls_addr_per_reg) for ls_addr_per_reg in ls_addr])
        MAX_REG_WRAP =  max([len(ls_addr_per_reg) for ls_addr_per_reg in ls_addr])
                
        # Create deserialization index map (in which deser register to write: addr -> wreg_sel)
        ls_wreg_idx = tuple([idx for ls_addr_per_reg in ls_addr for idx in range(len(ls_addr_per_reg))])
#        print "ls_wreg_idx  =", ls_wreg_idx

        # Write enable map: at which addresses we have to generate we to the actual register (the last address of a register)
        ls_wreg_we = tuple([1 if idx==len(ls_addr_per_reg)-1 else 0 for ls_addr_per_reg in ls_addr for idx in range(len(ls_addr_per_reg))])
#         print "ls_wreg_we  =", ls_wreg_we

        # Read enable map: at which addresses we have to generate re to the actual register (the first address of a register)
        ls_wreg_re = tuple([1 if idx==0 else 0 for ls_addr_per_reg in ls_addr for idx in range(len(ls_addr_per_reg))])
#         print "ls_wreg_re  =", ls_wreg_re

        # Select map: to which register an address belongs
        ls_wreg_sel = tuple([i for i, ls_addr_per_reg in enumerate(ls_addr) for _ in ls_addr_per_reg])
#        print "ls_wreg_sel  =", ls_wreg_sel


        # Register address High
#         ls_reg_addr_hi = tuple([ls_addr_per_reg[-1] for ls_addr_per_reg in ls_addr])
#         print "ls_reg_addr_hi =", ls_reg_addr_hi

        # Register address Low
#         ls_reg_addr_lo = tuple([ls_addr_per_reg[0] for ls_addr_per_reg in ls_addr])
#         print "ls_reg_addr_lo =", ls_reg_addr_lo

        # Register length in number of address cells occupied
#         ls_reg_len = tuple([len(ls_addr_per_reg)-1 for ls_addr_per_reg in ls_addr])
#         print "ls_reg_len =", ls_reg_len


        def bus_deserializer(rst, clk, wr_rdy, wr_vld, wr_addr, wr_data, ls_we, ls_wd):
            ''' Deserializes bus write access to registers: registers to address space, guarantees atomic register write
                    wr_rdy, wr_vld, wr_addr, wr_data - handshake interface for the write bus
                    ls_we - list of write enable signals, one signal per register
                    ls_wd - list of write data signals, one signal per register
                    Current behavior:
                        - Suppose we have:
                            - 20 bit register X
                            - 8 bit write data bus
                            - X is mapped to bus addresses:
                                X[ 7: 0] -> addr i
                                X[15: 8] -> addr i+1
                                X[19:16] -> addr i+2
                        - To write to X we have to do the following:
                            write(addr=i,   data=d0)
                            write(addr=i+1, data=d1)
                            write(addr=i+2, data=d2)
                            note: write(addr, data) represents bus transactions via the write bus interface (wr_rdy, wr_vld, wr_addr, wr_data)
                        - What happens under the hood:
                            write(addr=i,   data=X[ 7: 0]) - d0=X[ 7: 0] is written in an intermediate temporary register 0
                            write(addr=i+1, data=X[15: 8]) - d1=X[15: 8] is written in an intermediate temporary register 1
                            write(addr=i+2, data=X[19:16]) - d2=X[19:16] is written in an intermediate temporary register 2, and
                                                       d0, d1, d2 are transferred from the temporary registers to X (atomic write)
                            Write to X is triggered by write to addr i+2, the top address of a register. If we just write to i+2, without
                            before that writing to i and i+1, X will still be written with incorrect data from the temporary registers
                            TODO: May be, protect X such that write to it is executed only after i, i+1, i+2 are written sequentially
            '''

            NUM_STAGES  = 1

            stage0_en               = Signal(bool(0))
            stop0_rx                = Signal(bool(0))
            stop0_tx                = Signal(bool(0))

            pipe0_tx_vld = Signal(bool(0))
            pipe0_tx_rdy = Signal(bool(0))

            pipe0_ctrl_i = pipeline_control( rst             = rst,
                                             clk             = clk,
                                             rx_vld          = wr_vld,
                                             rx_rdy          = wr_rdy,
                                             tx_vld          = pipe0_tx_vld,
                                             tx_rdy          = pipe0_tx_rdy,
                                             stage_enable    = stage0_en,
                                             stop_rx         = [stop0_rx],
                                             stop_tx         = [stop0_tx] )

            # Temporary reg where the data is deserialized before writing it to the real register
            ls_treg = [Signal(intbv(0)[WBUS_WIDTH:]) for i in range(MAX_REG_WRAP)]
            treg = ConcatSignal(*reversed(ls_treg)) if (len(ls_treg) > 1) else ls_treg[0]
            # Selects the register being written
            reg_sel = Signal(intbv(0, min=0, max=NUM_REGS))

            """
            =============================================
            = Pipeline Stage 0
            =============================================
            """
            @always(clk.posedge)
            def S00_proc_wreg():
                ''' Deserialize '''
                if (rst):
                    stop0_rx.next    = 0
                    stop0_tx.next    = 1
                    reg_sel.next    = 0
                else:
                    if (stage0_en):
                        stop0_tx.next    = 1
                        for a in range(NUM_ADDR):
                            if (a == wr_addr):
                                # Deser
                                treg_idx = ls_wreg_idx[a]
                                we = ls_wreg_we[a]
                                sel = ls_wreg_sel[a]
                                ls_treg[treg_idx].next = wr_data
                                if (we==1):
                                    reg_sel.next    = sel
                                    stop0_tx.next   = 0

            def slicer(y,x):
                l = len(y)
                @always_comb
                def slicer_comb():
                    y.next = x[l:]
                return slicer_comb

            slc = [slicer(ls_wd[i], treg) for i in range(NUM_REGS)]

            @always_comb
            def we_demux():
                pipe0_tx_rdy.next = 1
                for i in range(NUM_REGS):
                    if (i == reg_sel):
                        ls_we[i].next = pipe0_tx_vld
                    else:
                        ls_we[i].next = 0

            return instances()

        busdeser = bus_deserializer(rst, clk, wr_rdy, wr_vld, wr_addr, wr_data, ls_we, ls_wd)


        def bus_serializer(rst, clk, ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data, ls_re, ls_rd):
            ''' Serializes bus read access to registers: maps registers to address space, guarantees atomic register read
                    ra_rdy, ra_vld, ra_data - input address handshake interface
                    rd_rdy, rd_vld, rd_data - output data handshake interface
                    ls_re - list of read enable signals, one signal per register
                    ls_rd - list of read data signals, on signal per register
                    Current behavior:
                        - Suppose we have:
                            - 20 bit register X
                            - 8 bit read data bus
                            - X is mapped to bus addresses:
                                X[ 7: 0] -> addr i
                                X[15: 8] -> addr i+1
                                X[19:16] -> addr i+2
                        - To read X we have to do the following:
                            d0 = read(addr=i)
                            d1 = read(addr=i+1)
                            d2 = read(addr=i+2)
                            note: read(addr) represents bus transactions via the read bus interface (ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data)
                        - What happens under the hood:
                            d0 = read(addr=i) - reads the whole X into an intermediate temporary register (atomic read), and
                                                returns d0 = X[ 7: 0]
                            d1 = read(addr=i+1) - reads d1 = X[15: 8] from the intermediate temporary register
                            d2 = read(addr=i+2) - reads d2 = X[19:16] from the intermediate temporary register

                            Reading X is triggered by a read from addr i, the first address of a register. If we just read from address i+1 or i+2
                            without before that reading from address i, we will be reading some dummy data from the intermediate temporary register.
                            TODO: May be, read X into the temporary register every time there is non-sequential access to some of the register addresses.
                            non-sequential access - registers are not accessed sequentially i, i+1, i+2
            '''

            NUM_STAGES  = 1

            stage1_en               = Signal(bool(0))
            stop1_rx                = Signal(bool(0))
            stop1_tx                = Signal(bool(0))

            pipe1_ctrl_i = pipeline_control( rst             = rst,
                                             clk             = clk,
                                             rx_vld          = ra_vld,
                                             rx_rdy          = ra_rdy,
                                             tx_vld          = rd_vld,
                                             tx_rdy          = rd_rdy,
                                             stage_enable    = stage1_en,
                                             stop_rx         = [stop1_rx],
                                             stop_tx         = [stop1_tx] )

            treg = Signal(intbv(0)[MAX_REG_WRAP*WBUS_WIDTH:])
            ls_treg = [Signal(intbv(0)[WBUS_WIDTH:]) for i in range(MAX_REG_WRAP)]

            def assigner(y,x):
                @always_comb
                def assigner_comb():
                    y.next = x
                return assigner_comb

            slc1 = [assigner(ls_treg[i], treg((i+1)*WBUS_WIDTH,i*WBUS_WIDTH)) for i in range(MAX_REG_WRAP)]


            reg_sel = Signal(intbv(0, min=0, max=NUM_REGS))

            """
            =============================================
            = Pipeline Stage 0
            =============================================
            """
            mux_sel = Signal(intbv(0, min=-1, max=MAX_REG_WRAP))

            def padder(y, x):
                @always_comb
                def padder_comb():
                    y.next = x
                return padder_comb

            ls_rdp = [Signal(intbv(0)[MAX_REG_WRAP*WBUS_WIDTH:]) for i in range(NUM_REGS)]
            pad = [assigner(ls_rdp[i], ls_rd[i]) for i in range(NUM_REGS)]

            @always(clk.posedge)
            def S10_proc_rreg():
                if (rst):
                    stop1_rx.next    = 0
                    stop1_tx.next    = 0
                else:
                    if (stage1_en):
                        for i in range(NUM_REGS):
                            ls_re[i].next = 0
                        if (not stop1_rx):
                            mux_sel.next = -1
                            for a in range(NUM_ADDR):
                                if (a == ra_data):
                                    treg_idx = ls_wreg_idx[a]
                                    mux_sel.next = treg_idx
                                    re = ls_wreg_re[a]
                                    sel = ls_wreg_sel[a]
                                    if (re==1):
                                        ls_re[sel].next = 1
                                        reg_sel.next   = sel
                                        stop1_rx.next   = 1
                                        stop1_tx.next   = 1
                        # TODO: Try using hs_mux to handle two data sources: addresses & regs
                        else:
                            treg.next        = ls_rdp[reg_sel]
                            stop1_rx.next    = 0
                            stop1_tx.next    = 0

            @always_comb
            def dat_mux():
                rd_data.next = 0xFFFFFFFF
                for i in range(MAX_REG_WRAP):
                    if (i == mux_sel):
                        rd_data.next = ls_treg[i]

            return instances()

        busser = bus_serializer(rst, clk, ra_rdy, ra_vld, ra_data, rd_rdy, rd_vld, rd_data, ls_re, ls_rd)

        return instances()
    
# -------------------------------------------------------------------------------------------------------------------------------------------------    

    def create_reg_file(self, rst, clk, filename=""):
        if self.reg_file:
            self.ctrl.create_address_map(self.BUS_DWIDTH, filename)
            return self.create_rd_wr_logic(rst, clk, self.interface_list[0], self.interface_list[1], self.interface_list[2], self.ctrl.ls, self.ctrl.ls_addr, filename)
        else:
            return []

