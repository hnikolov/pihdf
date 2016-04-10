import unittest

from myhdl_lib import *

from t_myvrlg import t_myvrlg

class Test_myvrlg(t_myvrlg):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_myvrlg.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_myvrlg.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_myvrlg.tearDown(self)

    # generate stimuli and reference data:
    def use_data_set_1(self):
        for i in range(16,26):
            self.stim_rx_hs.append({"data":i})
            self.ref_tx_hs.append({"data":i})

        self.run_it()
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Pass-through, generate test-vector files """
        self.models = {"top":self.BEH}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":50, "cosimulation":False, "trace":False, "fdump":True}
        self.use_data_set_1()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Pass-through test, using 'python-generated' stimuli """
        self.models = {"top":self.VRG}
        self.tb_config = {"simulation_time":50, "cosimulation":True, "trace":True, "fdump":False}
        self.use_data_set_1()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Pass-through test, using stimuli from test-vector files generated in test_001 """
        self.models = {"top":self.VRG}
        self.tb_config = {"simulation_time":50, "cosimulation":True, "trace":True, "fdump":False}
        self.use_data_from_files() # Files generated in test_001
