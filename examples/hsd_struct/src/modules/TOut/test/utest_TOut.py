import unittest

from myhdl_lib import *

from t_TOut import t_TOut

class Test_TOut(t_TOut):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_TOut.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_TOut.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_TOut.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Counting, duplicated output """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        self.stim_mode.append(  { "data":  0 })
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  0 }) # TODO: 1 cycle delay because we register 'mode'
 
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  0 })

        self.stim_inc_in.append({ "data":  1 })
        self.ref_LEDs.append(   { "data":  5 })

        self.stim_inc_in.append({ "data":  2 })
        self.ref_LEDs.append(   { "data": 10 })

        self.stim_inc_in.append({ "data":  3 })
        self.ref_LEDs.append(   { "data": 15 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Running light, left """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        self.stim_mode.append(  { "data":  1 })
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  0 }) # TODO: 1 cycle delay because we register 'mode'

        self.stim_inc_in.append({ "data":  1 })
        self.ref_LEDs.append(   { "data":  2 })

        self.stim_inc_in.append({ "data":  2 })
        self.ref_LEDs.append(   { "data":  4 })

        self.stim_inc_in.append({ "data":  3 })
        self.ref_LEDs.append(   { "data":  8 })

        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  1 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Running light, right """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":3, "ipgo":2}

        self.stim_mode.append(  { "data":  2 })
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  0 }) # TODO: 1 cycle delay because we register 'mode'

        self.stim_mode.append(  { "data":  2 })
        self.stim_inc_in.append({ "data":  1 })
        self.ref_LEDs.append(   { "data":  4 })

        self.stim_mode.append(  { "data":  2 })
        self.stim_inc_in.append({ "data":  2 })
        self.ref_LEDs.append(   { "data":  2 })

        self.stim_mode.append(  { "data":  2 })
        self.stim_inc_in.append({ "data":  3 })
        self.ref_LEDs.append(   { "data":  1 })

        self.stim_mode.append(  { "data":  2 })
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  8 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: Static output pattern """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":True, "fdump":False, "ipgi":3, "ipgo":2}

        self.stim_mode.append(  { "data":  3 })
        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data":  0 }) # TODO: 1 cycle delay because we register 'mode'

        self.stim_inc_in.append({ "data":  0 })
        self.ref_LEDs.append(   { "data": 21 })

        self.stim_inc_in.append({ "data":  1 })
        self.ref_LEDs.append(   { "data": 21 })

        self.run_it()

    # ----------------------------------------------------------------------------
