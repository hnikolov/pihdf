import unittest

from myhdl_lib import *

from t_hsd_inc import t_hsd_inc

class Test_hsd_inc(t_hsd_inc):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_hsd_inc.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_hsd_inc.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_hsd_inc.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Test with data in the range 30-40 """

        self.models = {"top":self.BEH}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(30, 40):
            self.stim_rxd.append({"data": i  })
            self.ref_txd.append( {"data": i+1})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Test with data in the range 30-40 """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(30, 40):
            self.stim_rxd.append({"data": i  })
            self.ref_txd.append( {"data": i+1})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Test with data in the range 30-40 """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        for i in range(30, 40):
            self.stim_rxd.append({"data": i  })
            self.ref_txd.append( {"data": i+1})

        self.run_it()

    # ----------------------------------------------------------------------------
