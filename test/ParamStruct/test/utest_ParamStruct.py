import unittest

from myhdl_lib import *

from t_ParamStruct import t_ParamStruct

class Test_ParamStruct(t_ParamStruct):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_ParamStruct.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_ParamStruct.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_ParamStruct.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Use top parameters default values, and local parameters """

#         self.dut_params = {"TOP_PARAM_NONE":None, "TOP_PARAM_BOOL":True, "TOP_PARAM_INT":10, "TOP_PARAM_FLOAT":1.5, "TOP_PARAM_STR":'my_string_A'}
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        # TO DO: generate stimuli and reference data here

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Set top parameters explicitly, and use also local parameters """

        self.dut_params = {"TOP_PARAM_NONE":None, "TOP_PARAM_BOOL":False, "TOP_PARAM_INT":20, "TOP_PARAM_FLOAT":2.5, "TOP_PARAM_STR":'my_string_B'}
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        # TO DO: generate stimuli and reference data here

        self.run_it()

    # ----------------------------------------------------------------------------
