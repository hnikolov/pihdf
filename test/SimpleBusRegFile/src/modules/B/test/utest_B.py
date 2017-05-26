import unittest

from myhdl_lib import *

from t_B import t_B

class Test_B(t_B):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_B.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_B.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_B.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: TO DO: describe the test """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        fields_in = { 'addr': 0, 'data': 11 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 1, 'data': 22 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 3, 'data': 33 }
        self.stim_sbus_wa_wd.append( fields_in )

        fields_in = { 'addr': 4, 'data': 44 }
        self.stim_sbus_wa_wd.append( fields_in )

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", len(self.stim_sbus_wa_wd)-1))]

        self.stim_sbus_raddr.append({"data":  0})
        self.ref_sbus_rdata.append( {"data": 33}) # Register value = value + global register

        self.stim_sbus_raddr.append({"data":  1})
        self.ref_sbus_rdata.append( {"data":  0}) # Global reg, write only, read returns 0

        self.stim_sbus_raddr.append({"data":  3})
        self.ref_sbus_rdata.append( {"data": 33})

        self.stim_sbus_raddr.append({"data":  4})
        self.ref_sbus_rdata.append( {"data":  0}) # Write only, read returns 0
        
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_002(self):
        """ >>>>>> TEST_002: Testing write-only/read-only registers, FIFO """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        # Write 5 values to the FIFO @ address 4 (FIFO size=4 -> the last value is dropped)
        for i in range(11, 16):
            fields_in = { 'addr': 4, 'data': i }
            self.stim_sbus_wa_wd.append( fields_in )

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", len(self.stim_sbus_wa_wd)-1))]

        # Read 4 values from the FIFO @ address 5
        for i in range(11, 15):
            self.stim_sbus_raddr.append({"data": 5})
            self.ref_sbus_rdata.append( {"data": i})

        # Another read: FIFO is empty -> data == first element (but not valid)
        self.stim_sbus_raddr.append({"data":  5})
        self.ref_sbus_rdata.append( {"data": 11})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_003(self):
        """ >>>>>> TEST_003: All registers are accessible """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 6

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            data = 10+i
            self.stim_sbus_wa_wd.append({ 'addr': i, 'data': data })
            ref.append(data)

        # Set the global register to 0
        fields_in = { 'addr': 1, 'data': 0 }
        self.stim_sbus_wa_wd.append( fields_in )

        # Global register (read_only)
        ref[1] = 0
        
        # Read_only = Write_only
        ref[5] = ref[4]
        
        # Write_only = 0
        ref[4] = 0

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", len(self.stim_sbus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_sbus_raddr.append({"data": i})
            self.ref_sbus_rdata.append( {"data": ref[i]})

        # Read outside the address space
        self.stim_sbus_raddr.append({"data": NUM_ADDR})
        self.ref_sbus_rdata.append( {"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_004(self):
        """ >>>>>> TEST_004: All register sizes are correct """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 6
        data = 0xFFFFFFFF

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            self.stim_sbus_wa_wd.append({ 'addr':i, 'data': data })
            ref.append(data)

        # Set the global register to 0
        fields_in = { 'addr': 1, 'data': 0 }
        self.stim_sbus_wa_wd.append( fields_in )

        # Global register (read_only)
        ref[1] = 0
        
        # Read_only = Write_only
        ref[5] = ref[4]

        # Write_only = 0
        ref[4] = 0

        # "Small" registers (24 bit)
        ref[2] = 0x00FFFFFF

        self.cond_sbus_raddr += [(0,("sbus_wa_wd", len(self.stim_sbus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_sbus_raddr.append({"data": i})
            self.ref_sbus_rdata.append({"data": ref[i]})

        # Read outside the address space
        self.stim_sbus_raddr.append({"data": NUM_ADDR})
        self.ref_sbus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()        
    # ----------------------------------------------------------------------------
