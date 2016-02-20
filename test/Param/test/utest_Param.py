import unittest

from myhdl_lib import *

from t_Param import t_Param

class Test_Param(t_Param):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_Param.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_Param.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_Param.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Use default parameters """

#         self.dut_params = {"PARAM_NONE":None, "PARAM_BOOL":True, "PARAM_INT":10, "PARAM_FLOAT":1.5, "PARAM_STR":"my_string_A"}
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        # TO DO: generate stimuli and reference data here

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Set parameters """

        self.dut_params = {"PARAM_NONE":None, "PARAM_BOOL":False, "PARAM_INT":20, "PARAM_FLOAT":2.5, "PARAM_STR":"my_string_B"}
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        # TO DO: generate stimuli and reference data here

        self.run_it()

    # ----------------------------------------------------------------------------
