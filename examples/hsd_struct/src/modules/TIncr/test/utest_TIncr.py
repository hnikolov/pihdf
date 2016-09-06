import unittest

from myhdl_lib import *

from t_TIncr import t_TIncr

class Test_TIncr(t_TIncr):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_TIncr.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_TIncr.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_TIncr.tearDown(self)


    # ----------------------------------------------------------------------------
    @unittest.skip("Test was used for checking the functionality when mode=1 by observing the traces. Formal check fails")
    def test_000(self):
        """ >>>>>> TEST_000: TODO """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(0, 20):
            self.stim_mode.append({ "data": 1 })
            self.ref_inc_out.append({ "data": (i+1) % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Modulo 4 count """

        self.models = {"top":self.RTL}
        self.dut_params = {"DELAY_BITS":2}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(0, 40):
            self.stim_mode.append({ "data": 0 })

        for i in range(0, 10): # Pre-scale = 4 (2 delay bits) => 10 output data for 10*4=40 mode cycles
            self.ref_inc_out.append({ "data": i % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Modulo 4 count TODO: check the first hsd_en in traces. Should not be there !!! """

        self.models = {"top":self.RTL}
        self.dut_params = {"DELAY_BITS":2}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":5}

        for i in range(0, 40):
            self.stim_mode.append({ "data": 0 })

        for i in range(0, 10): # Pre-scale = 4 (2 delay bits) => 10 output data for 10*4=40 mode cycles
            self.ref_inc_out.append({ "data": i % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Modulo 4 count DELAY_BITS=0 -> skip delay counter """

        self.models = {"top":self.RTL}
        self.dut_params = {"DELAY_BITS":0}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(0, 10): 
            self.stim_mode.append(  { "data": 0     })
            self.ref_inc_out.append({ "data": i % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
