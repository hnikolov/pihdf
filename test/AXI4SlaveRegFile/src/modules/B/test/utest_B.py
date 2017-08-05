import unittest

from myhdl_lib import *

from t_B import t_B

class Test_B(t_B):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_B.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_B.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_B.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: TO DO: describe the test """

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

        self.stim_sbus_waddr.append({"data": 4*4})
        self.stim_sbus_wdata.append({"data": 55, "strobes": 0xF})
        self.ref_sbus_wresp.append({"data": 0})

        # Start reading only after the last write response is received
        self.cond_sbus_raddr.append((0,("sbus_wresp", 3)))

        self.stim_sbus_raddr.append({"data": 4*0})
        self.ref_sbus_rdata.append({"data": 11, "response": 0})

        self.stim_sbus_raddr.append({"data": 4*1})
        self.ref_sbus_rdata.append({"data": 0, "response": 0}) # Write only, read returns 0

        self.stim_sbus_raddr.append({"data": 4*2})
        self.ref_sbus_rdata.append({"data": 33, "response": 0})

        self.stim_sbus_raddr.append({"data": 4*4})
        self.ref_sbus_rdata.append({"data": 0, "response": 0}) # Write only, read returns 0

        self.stim_sbus_raddr.append({"data": 4*5})
        self.ref_sbus_rdata.append({"data": 55, "response": 0}) # Read only (by design presents the value written in at addr 4)

        self.run_it()


    # ----------------------------------------------------------------------------
