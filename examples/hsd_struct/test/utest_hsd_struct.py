import unittest

from myhdl_lib import *

from t_hsd_struct import t_hsd_struct

class Test_hsd_struct(t_hsd_struct):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_hsd_struct.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_hsd_struct.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_hsd_struct.tearDown(self)


    # Initialise data, duplicate output
    def init_data_dupl(self):
        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 5  })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 10 })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 15 })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 0  })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 5  })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 10 })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 15 })

        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 0  })
        self.ref_LEDs.append(   { "data": 0  })

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Counting, duplicated output """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        self.init_data_dupl()
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Counting, duplicated output """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":2, "ipgo":0}

        self.init_data_dupl()
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Counting, duplicated output """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":True, "fdump":False, "ipgi":0, "ipgo":4}

        self.init_data_dupl()
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: Counting, duplicated output """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":3}

        self.init_data_dupl()
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_005(self):
        """ >>>>>> TEST_005: Running light, left """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        self.stim_mode_1.append({ "data": 0 })
        self.stim_mode_2.append({ "data": 1 }) # Registered in TOut
        self.ref_LEDs.append(   { "data": 2 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 4 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 8 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 1 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 2 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 4 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_006(self):
        """ >>>>>> TEST_006: Running light, right """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        self.stim_mode_1.append({ "data": 0 })
        self.stim_mode_2.append({ "data": 2 }) # Registered in TOut
        self.ref_LEDs.append(   { "data": 4 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 2 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 1 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 8 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 4 })

        self.stim_mode_1.append({ "data": 0 })
        self.ref_LEDs.append(   { "data": 2 })

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_007(self):
        """ >>>>>> TEST_007: static pattern. Note: Change the output from the incrementor for synthesis! """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":2}


        self.stim_mode_1.append({ "data": 0  })
        self.stim_mode_2.append({ "data": 3  })
        self.ref_LEDs.append(   { "data": 21 })

        self.stim_mode_1.append({ "data": 1  })
        self.stim_mode_2.append({ "data": 3  })
        self.ref_LEDs.append(   { "data": 21 })

        self.run_it()

    # ----------------------------------------------------------------------------
