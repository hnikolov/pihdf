import unittest

from myhdl_lib import *

from t_AXI4SlaveRegFile import t_AXI4SlaveRegFile

class Test_AXI4SlaveRegFile(t_AXI4SlaveRegFile):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_AXI4SlaveRegFile.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_AXI4SlaveRegFile.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_AXI4SlaveRegFile.tearDown(self)

    def AXI_write(self, addr, data):
        self.cond_sbus_waddr.append((len(self.stim_sbus_waddr),("sbus_rdata", len(self.ref_sbus_rdata)-1))) # After the last read
        self.cond_sbus_wdata.append((len(self.stim_sbus_wdata),("sbus_rdata", len(self.ref_sbus_rdata)-1))) # After the last read

        self.stim_sbus_waddr.append({"data": addr})
        self.stim_sbus_wdata.append({"data": data, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})
 
    def AXI_read(self, addr, data):
        self.cond_sbus_raddr.append((len(self.stim_sbus_raddr),("sbus_wresp", len(self.ref_sbus_wresp)-1))) # After the last write

        self.stim_sbus_raddr.append({"data": addr})
        self.ref_sbus_rdata.append({"data": data, "response": 0})


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Testing write/read registers """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":600, "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        addrw = [ 0,  2,  3,  4,  5,  6,  7,  8, 10, 11, 12, 13, 30]  # + writing to a wrong address: 30
        addrr = [ 0,  2,  3,  4,  5,  6,  7,  9, 10, 11, 12, 14]
        data  = [11, 22, 33, 44, 55, 66, 77, 88, 99, 98, 97, 96, 96]

        for a, d in zip(addrw, data):
            self.AXI_write(addr=4*a, data=d)
#             self.stim_sbus_waddr.append({"data": a})
#             self.stim_sbus_wdata.append({"data": d, "strobes": 0xF})
#             self.ref_sbus_wresp.append({"data": 0})

        # WRITE TO ALL INSTANCES OF THE GLOBAL REGISTER
        self.AXI_write(addr=4*1, data=111)
#         self.stim_sbus_waddr.append({"data": 1})
#         self.stim_sbus_wdata.append({"data": 111, "strobes": 0xF})
#         self.ref_sbus_wresp.append({"data": 0})

        # Start reading only after the last write response is received
#         self.cond_sbus_raddr.append((0,("sbus_wresp", len(self.ref_sbus_wresp)-1)))

        for a, d in zip(addrr, data):
            self.AXI_read(addr=4*a, data=d)
#             self.stim_sbus_raddr.append({"data": a})
#             self.ref_sbus_rdata.append({"data": d, "response": 0})

        self.AXI_read(addr=4*30, data=0xFFFFFFFF)  # WRONG ADDRESS: ref data assigned to 0
#         self.stim_sbus_raddr.append({"data": 30})  # WRONG ADDRESS: ref data assigned to 0
#         self.ref_sbus_rdata.append({"data": 0xFFFFFFFF, "response": 0})

        self.run_it()
    # ----------------------------------------------------------------------------
