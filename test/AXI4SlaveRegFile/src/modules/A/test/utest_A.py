import unittest

from myhdl_lib import *

from t_A import t_A

class Test_A(t_A):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_A.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_A.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_A.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: Raw bus access """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":150, "cosimulation":True, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        self.stim_sbus_waddr.append({"data": 4*0})
        self.stim_sbus_wdata.append({"data": 11, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})

        self.stim_sbus_waddr.append({"data": 4*1})
        self.stim_sbus_wdata.append({"data": 22, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})

        self.stim_sbus_waddr.append({"data": 4*2})
        self.stim_sbus_wdata.append({"data": 33, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})

        self.stim_sbus_waddr.append({"data": 4*13})  # WRONG ADDRESS
        self.stim_sbus_wdata.append({"data": 77, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})

        # Start reading only after the last write response is received
        self.cond_sbus_raddr.append((0,("sbus_wresp", 3)))

        self.stim_sbus_raddr.append({"data": 4*0})
        self.ref_sbus_rdata.append({"data": 11, "response": 0})

        self.stim_sbus_raddr.append({"data": 4*1})
        self.ref_sbus_rdata.append({"data": 0, "response": 0})  # Global register is declared as write only

        self.stim_sbus_raddr.append({"data": 4*2})
        self.ref_sbus_rdata.append({"data": 33, "response": 0})

        self.stim_sbus_raddr.append({"data": 4*13})
        self.ref_sbus_rdata.append({"data": 0xFFFFFFFF, "response": 0})

        self.run_it()
    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Func bus access """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":150, "cosimulation":True, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        def AXI_write(addr, data):
            self.cond_sbus_waddr.append((len(self.stim_sbus_waddr),("sbus_rdata", len(self.ref_sbus_rdata)-1))) # After the last read
            self.cond_sbus_wdata.append((len(self.stim_sbus_wdata),("sbus_rdata", len(self.ref_sbus_rdata)-1))) # After the last read

            self.stim_sbus_waddr.append({"data": addr})
            self.stim_sbus_wdata.append({"data": data, "strobes": 0xF})
            self.ref_sbus_wresp.append({"data": 0})

        def AXI_read(addr, data):
            self.cond_sbus_raddr.append((len(self.stim_sbus_raddr),("sbus_wresp", len(self.ref_sbus_wresp)-1))) # After the last write

            self.stim_sbus_raddr.append({"data": addr})
            self.ref_sbus_rdata.append({"data": data, "response": 0})



#         self.stim_sbus_waddr.append({"data": 0})
#         self.stim_sbus_wdata.append({"data": 11, "strobes": 0xF})
#         self.ref_sbus_wresp.append({"data": 0})
        AXI_write(addr=4*0, data=11)

#         self.stim_sbus_waddr.append({"data": 1})
#         self.stim_sbus_wdata.append({"data": 22, "strobes": 0xF})
#         self.ref_sbus_wresp.append({"data": 0})
        AXI_write(addr=4*1, data=22)

#         self.stim_sbus_waddr.append({"data": 2})
#         self.stim_sbus_wdata.append({"data": 33, "strobes": 0xF})
#         self.ref_sbus_wresp.append({"data": 0})
        AXI_write(addr=4*2, data=33)

#         self.stim_sbus_waddr.append({"data": 13})  # WRONG ADDRESS
#         self.stim_sbus_wdata.append({"data": 77, "strobes": 0xF})
#         self.ref_sbus_wresp.append({"data": 0})
        AXI_write(addr=4*13, data=77)  # WRONG ADDRESS

##         Start reading only after the last write response is received
#         self.cond_sbus_raddr.append((0,("sbus_wresp", 3)))

#         self.stim_sbus_raddr.append({"data": 0})
#         self.ref_sbus_rdata.append({"data": 11, "response": 0})
        AXI_read(addr=4*0, data=11)

#         self.stim_sbus_raddr.append({"data": 1})
#         self.ref_sbus_rdata.append({"data": 0, "response": 0})  # Global register is declared as write only
        AXI_read(addr=4*1, data=0)  # Global register is declared as write only

#         self.stim_sbus_raddr.append({"data": 2})
#         self.ref_sbus_rdata.append({"data": 33, "response": 0})
        AXI_read(addr=4*2, data=33)

#         self.stim_sbus_raddr.append({"data": 13})
#         self.ref_sbus_rdata.append({"data": 0xFFFFFFFF, "response": 0})
        AXI_read(addr=4*13, data=0xFFFFFFFF)

        self.run_it()
    # ----------------------------------------------------------------------------
