import unittest

from myhdl_lib import *

from t_hsd_custom import t_hsd_custom

class Test_hsd_custom(t_hsd_custom):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_hsd_custom.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_hsd_custom.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_hsd_custom.tearDown(self)

    # generate stimuli and reference data:
    def use_data_set_1(self):
        fields_in = { 'cmd': 1, 'port': 2000 }
        self.stim_rx_port_flds.append( fields_in )
        self.ref_tx_port_flds.append( fields_in )

        fields_in = { 'cmd': 0, 'port': 3000 }
        self.stim_rx_port_flds.append( fields_in )
        self.ref_tx_port_flds.append( fields_in )

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Dump data to files """

        self.models = {"top":self.BEH}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":False, "trace":False, "fdump":True}
        self.use_data_set_1()
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: The same stimuli as in test_001 """

        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":150, "cosimulation":False, "trace":True, "fdump":False}
        self.use_data_set_1()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: The same stimuli as in test_001 """

        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":150, "cosimulation":True, "trace":True, "fdump":False}
        self.use_data_set_1()

    # ----------------------------------------------------------------------------
    #@unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: The same stimuli as in test_001 but all stimuli and expected results read from files """

        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":150, "cosimulation":False, "trace":True, "fdump":False}
        self.use_data_from_files()
        
    # ----------------------------------------------------------------------------
    #@unittest.skip("")
    def test_005(self):
        """ >>>>>> TEST_005: The same stimuli as in test_001 but all stimuli and expected results read from files """

        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False}
        self.use_data_from_files()
        
