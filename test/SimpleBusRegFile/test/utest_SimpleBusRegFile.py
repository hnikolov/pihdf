import unittest

from myhdl_lib import *

from t_SimpleBusRegFile import t_SimpleBusRegFile

class Test_SimpleBusRegFile(t_SimpleBusRegFile):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_SimpleBusRegFile.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_SimpleBusRegFile.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_SimpleBusRegFile.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Testing write/read registers """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        data = [11, 22, 33, 44, 55, 66, 77, 88, 99]

#        for j,i in enumerate([0, 6, 11, 16, 19, 24, 30]): # + writing to a wrong address: 30
        for j,i in enumerate([0, 12, 3, 4, 5, 6, 7, 30]): # + writing to a wrong address: 30
            fields_in = { 'addr': i, 'data': data[j] }
            self.stim_simple_bus_wa_wd.append( fields_in )

        # WRITE TO ALL INSTANCES OF THE GLOBAL REGISTER
        fields_in = { 'addr': 1, 'data': 111 }
        self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for j,i in enumerate([0, 12, 3, 4, 5, 6, 7]):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": data[j]})

        self.stim_simple_bus_raddr.append({"data": 30}) # WRONG ADDRESS: ref data assigned to 0
        self.ref_simple_bus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_002(self):
        """ >>>>>> TEST_002: Testing write-only/read-only registers """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        data = [11, 22, 33, 44, 55, 66, 77]

        for j,i in enumerate([8, 13]):
            fields_in = { 'addr': i, 'data': data[j] }
            self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for j,i in enumerate([9, 14]):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": data[j]})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_003(self):
        """ >>>>>> TEST_003: All registers are accessible """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 15

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            data = 10+i
            self.stim_simple_bus_wa_wd.append( { 'addr':i, 'data': data } )
            ref.append(data)

        # Global register (read_only)
        ref[1] = 0
        
        # Read_only = Write_only
        ref[9], ref[14] = ref[8], ref[13]
        
        # Write_only = 0
        ref[8], ref[13] = 0, 0

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": ref[i]})
        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_004(self):
        """ >>>>>> TEST_004: All register sizes are correct """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 15

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            data = 0xFFFFFFFF
            self.stim_simple_bus_wa_wd.append( { 'addr':i, 'data': data } )
            ref.append(data)

        # Global register (read_only)
        ref[1] = 0
        
        # Read_only = Write_only
        ref[9], ref[14] = ref[8], ref[13]

        # Write_only = 0
        ref[8], ref[13] = 0, 0

        # "Small" registers (24 bit)
        ref[2] = ref[4] = ref[6] = ref[11] = 0x00FFFFFF

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": ref[i]})
        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()
