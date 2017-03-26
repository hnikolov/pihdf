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
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        fields_in = { 'addr': 0, 'data': 11 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 0, 'data': 22 }
        self.stim_sbus_wa_wd.append( fields_in )

        #--- big_register --
#        fields_in = { 'addr': 3, 'data':1}
#        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 4, 'data': 2 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 5, 'data': 3 }
        self.stim_sbus_wa_wd.append( fields_in )
        #---

        fields_in = { 'addr': 13, 'data': 33 }  # WRONG ADDRESS
        self.stim_sbus_wa_wd.append( fields_in )

        self.cond_sbus_wa_wd += [(1,("sbus_raddr", 0)),
                                 (2,("sbus_raddr", 1))]

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", 0)),
                                 (1,("sbus_wa_wd", 1)),
                                 (2,("sbus_wa_wd", 4)),
                                 (5,("sbus_wa_wd", 5))]

        self.stim_sbus_raddr.append({"data": 0})
        self.stim_sbus_raddr.append({"data": 0})
#        self.stim_sbus_raddr.append({"data": 3})
        self.stim_sbus_raddr.append({"data": 4})
        self.stim_sbus_raddr.append({"data": 5})
        self.stim_sbus_raddr.append({"data": 13}) # WRONG ADDRESS: No response - no ref data assigned

        self.ref_sbus_rdata.append({"data": 11})
        self.ref_sbus_rdata.append({"data": 22})
#        self.ref_sbus_rdata.append({"data": 1})
        self.ref_sbus_rdata.append({"data": 2})
        self.ref_sbus_rdata.append({"data": 3})
        self.ref_sbus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
