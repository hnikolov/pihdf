import unittest

from myhdl_lib import *

from t_C import t_C

class Test_C(t_C):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_C.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_C.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_C.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: Registers access, FIFO write/read """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        fields_in = { 'addr': 0, 'data': 11 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 1, 'data': 22 }
        self.stim_sbus_wa_wd.append( fields_in )

        # write only -> FIFO write
        fields_in = { 'addr': 4, 'data': 33 }
        self.stim_sbus_wa_wd.append( fields_in )
        fields_in = { 'addr': 4, 'data': 44 }
        self.stim_sbus_wa_wd.append( fields_in )

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", len(self.stim_sbus_wa_wd)-1))]

        self.stim_sbus_raddr.append({"data":  0})
        self.ref_sbus_rdata.append( {"data": 33}) # Register value = value + global register

        self.stim_sbus_raddr.append({"data": 1})
        self.ref_sbus_rdata.append( {"data": 0}) # Global reg, write only, read returns 0

        self.stim_sbus_raddr.append({"data": 4})
        self.ref_sbus_rdata.append( {"data": 0}) # Write only, read returns 0

        # Read only -> FIFO read
        self.stim_sbus_raddr.append({"data":  5})
        self.ref_sbus_rdata.append( {"data": 33})
        self.stim_sbus_raddr.append({"data":  5})
        self.ref_sbus_rdata.append( {"data": 44})
        
        self.run_it()

    # ----------------------------------------------------------------------------
