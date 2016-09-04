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

        for i in range(0, 10):
            self.stim_mode.append({ "data": 1 })
            self.ref_inc_out.append({ "data": (i+1) % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Modulo 4 count """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(0, 10):
            self.stim_mode.append(  { "data": 0         })
            self.ref_inc_out.append({ "data": (i+1) % 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
