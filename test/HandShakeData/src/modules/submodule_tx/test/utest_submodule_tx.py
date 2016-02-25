import unittest

from myhdl_lib import *

from t_submodule_tx import t_submodule_tx

class Test_submodule_tx(t_submodule_tx):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_submodule_tx.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_submodule_tx.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_submodule_tx.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: TO DO: describe the test """

        self.models = {"top":self.BEH}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        # TO DO: generate stimuli and reference data here

        self.run_it()

    # ----------------------------------------------------------------------------
