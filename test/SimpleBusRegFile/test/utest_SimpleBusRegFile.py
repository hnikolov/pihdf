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
    def test_000(self):
        """ >>>>>> TEST_000: Testing registers, global register = 0 """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        address = [ 0, 12,  3,  4,  5,  6,  7]
        data    = [11, 22, 33, 44, 55, 66, 77]
        
        for a, d in zip(address, data): # + writing to a wrong address: 30
            fields_in = { 'addr': a, 'data': d }
            self.stim_simple_bus_wa_wd.append( fields_in )

        # Write to a wrong address
        fields_in = { 'addr': 30, 'data': 88 }
        self.stim_simple_bus_wa_wd.append( fields_in )

        # Write to all instances of the global register
        fields_in = { 'addr': 1, 'data': 0 }
        self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]
        
        # Read
        for a, d in zip(address, data):
            self.stim_simple_bus_raddr.append({"data": a})
            self.ref_simple_bus_rdata.append( {"data": d})

        self.stim_simple_bus_raddr.append({"data": 30}) # WRONG ADDRESS
        self.ref_simple_bus_rdata.append( {"data": 0xFFFFFFFF})

        self.stim_simple_bus_raddr.append({"data": 1}) # Global register is write only
        self.ref_simple_bus_rdata.append( {"data": 0})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Testing write/read all registers, global register != 0 """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        # Write to all registers, including read-only as wel; 1 "wrong" register (address 30)
        # Use global register value, e.g., address 0: 232 = 11 + 221
        address = [  0,   1,  2,   3,  4,   5,  6,  7,  8,  9, 10,   11,  12,  13,  14,  30]
        data_wr = [ 11, 221, 22,  33, 44,  55, 66, 77, 88, 99, 110, 111, 112, 113, 114, 330]
        data_rd = [232,   0, 22, 254, 44, 276, 66, 77,  0, 88, 331, 111, 112,   0, 113, 0xFFFFFFFF]

        # Write
        for a, d in zip(address, data_wr):
            fields_in = { 'addr': a, 'data': d }
            self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        # Read
        for a, d in zip(address, data_rd):
            self.stim_simple_bus_raddr.append({"data": a})
            self.ref_simple_bus_rdata.append( {"data": d})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_002(self):
        """ >>>>>> TEST_002: Testing write-only/read-only registers (FIFOs) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        # FIFO size is 4
        addr_wr = [  8,  8,  8,  8, 13, 13, 13, 13, 13] # Attempt write to a full FIFO (13)
        addr_rd = [  9,  9,  9,  9, 14, 14, 14, 14, 14] # Read from an empty FIFO
        data =    [ 11, 22, 33, 44, 55, 66, 77, 88, 55] # The last 55 is not valid data: FIFO is empty

        for a, d in zip(addr_wr, data):
            fields_in = { 'addr': a, 'data': d }
            self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for a, d in zip(addr_rd, data):
            self.stim_simple_bus_raddr.append({"data": a})
            self.ref_simple_bus_rdata.append( {"data": d})

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

        # Set the global register to 0
        fields_in = { 'addr': 1, 'data': 0 }
        self.stim_simple_bus_wa_wd.append( fields_in )

        # Global register (read_only)
        ref[1] = 0
        
        # Read_only = Write_only
        ref[9], ref[14] = ref[8], ref[13]
        
        # Write_only = 0
        ref[8], ref[13] = 0, 0

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append ({"data": ref[i]})

        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append( {"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("TODO")
    def test_004(self):
        """ >>>>>> TEST_004: All register sizes are correct """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 15
        data = 0xFFFFFFFF

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            self.stim_simple_bus_wa_wd.append( { 'addr':i, 'data': data } )
            ref.append(data)

        # Set the global register to 0
        fields_in = { 'addr': 1, 'data': 0 }
        self.stim_simple_bus_wa_wd.append( fields_in )

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
            self.ref_simple_bus_rdata.append( {"data": ref[i]})

        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append( {"data": 0xFFFFFFFF})

        self.run_it()
