import unittest

from myhdl_lib import *

from t_A import t_A

class Test_A(t_A):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_A.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_A.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_A.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: TO DO: describe the test """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":150, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

        fields_in = { 'addr': 0, 'data': 11 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 1, 'data': 22 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 2, 'data': 2 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 13, 'data': 33 }  # WRONG ADDRESS
        self.stim_sbus_wa_wd.append( fields_in )

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", 3))]

        self.stim_sbus_raddr.append({"data":  0})
        self.ref_sbus_rdata.append( {"data": 33}) # register + global register

        self.stim_sbus_raddr.append({"data": 1})
        self.ref_sbus_rdata.append( {"data": 0})  # Global register is declared as write only

        self.stim_sbus_raddr.append({"data": 2})
        self.ref_sbus_rdata.append( {"data": 2})

        self.stim_sbus_raddr.append({"data": 13}) # WRONG ADDRESS: No response - no ref data assigned
        self.ref_sbus_rdata.append( {"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
