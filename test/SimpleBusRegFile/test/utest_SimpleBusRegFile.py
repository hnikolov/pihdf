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
        self.tb_config = {"simulation_time":600, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}

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
    @unittest.skip("TODO")
    def test_002(self):
        """ >>>>>> TEST_002: Testing write-only/read-only registers """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        data = [11, 22, 33, 44, 55, 66, 77]

        for j,i in enumerate([17, 25]):
            fields_in = { 'addr': i, 'data': data[j] }
            self.stim_simple_bus_wa_wd.append( fields_in )

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for j,i in enumerate([18, 26]):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": data[j]})

        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("TODO")
    def test_003(self):
        """ >>>>>> TEST_003: All registers are accessible """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 27

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            data = 10+i
            self.stim_simple_bus_wa_wd.append( { 'addr':i, 'data': data } )
            ref.append(data)

        # Global register (read_only)
        ref[1] = 0

        # Read_only, Write_only
        ref[18], ref[26] = ref[17], ref[25]
        ref[17], ref[25] = 0, 0

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": ref[i]})
        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("TODO")
    def test_004(self):
        """ >>>>>> TEST_004: All register sizes are correct """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        NUM_ADDR = 27

        ref = []
        for i in range(NUM_ADDR+1): # One extra data word written outside the address space
            data = 0xFFFFFFFF
            self.stim_simple_bus_wa_wd.append( { 'addr':i, 'data': data } )
            ref.append(data)

        # Global register (read_only)
        ref[1] = 0

        # Read_only, Write_only
        ref[18], ref[26] = ref[17], ref[25]
        ref[17], ref[25] = 0, 0

        # "Small" registers (24 bit)
        ref[2] = ref[7] = ref[12] = ref[20] = 0x00FFFFFF

        # "Big" registers (80 bit) top word
        ref[5] = ref[10] = ref[15] = ref[23] = 0x0000FFFF

        self.cond_simple_bus_raddr += [(0,("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for i in range(NUM_ADDR):
            self.stim_simple_bus_raddr.append({"data": i})
            self.ref_simple_bus_rdata.append({"data": ref[i]})
        # Read outside the address space
        self.stim_simple_bus_raddr.append({"data": NUM_ADDR})
        self.ref_simple_bus_rdata.append({"data": 0xFFFFFFFF})

        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("TODO")
    def test_005(self):
        """ >>>>>> TEST_005: 'Big' registers are written atomically when writing their top address """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        big_regs = [[3,4,5],[8,9,10],[13,14,15],[21,22,23]]
        # "Big" register @3,4,5
        good_data = [10,11,12]
        bad_data  = [20,21,22]

        # Write all big registers
        for reg in big_regs:
            for i,addr in enumerate(reg):
                self.stim_simple_bus_wa_wd.append( { 'addr':addr, 'data': good_data[i] } )

        # After writing to all big registers
        self.cond_simple_bus_raddr += [(len(self.stim_simple_bus_raddr),("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for reg in big_regs:
            for i,addr in enumerate(reg):
                self.stim_simple_bus_raddr.append({"data": addr})
                self.ref_simple_bus_rdata.append({"data": good_data[i]})

        # After reading all big registers
        self.cond_simple_bus_wa_wd += [(len(self.stim_simple_bus_wa_wd),("simple_bus_rdata", len(self.ref_simple_bus_rdata)-1))]

        # This should not write to the big regs, because their top address is not written
        for reg in big_regs:
            for i,addr in enumerate(reg):
                if i < 2:
                    self.stim_simple_bus_wa_wd.append( { 'addr':addr, 'data': bad_data[i] } )

        # After writing all big registers
        self.cond_simple_bus_raddr += [(len(self.stim_simple_bus_raddr),("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        # Should read the old good_data
        for reg in big_regs:
            for i,addr in enumerate(reg):
                self.stim_simple_bus_raddr.append({"data": addr})
                self.ref_simple_bus_rdata.append({"data": good_data[i]})


        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("TODO")
    def test_006(self):
        """ >>>>>> TEST_006: 'Big' registers are read atomically when reading their lowest address """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        big_regs = [[3,4,5],[8,9,10],[13,14,15],[21,22,23]]
        # "Big" register @3,4,5
        good_data = [10,11,12]
        bad_data  = [20,21,22]

        # Write all big registers
        for reg in big_regs:
            for i,addr in enumerate(reg):
                self.stim_simple_bus_wa_wd.append( { 'addr':addr, 'data': good_data[i] } )

        # After writing to all registers
        self.cond_simple_bus_raddr += [(len(self.stim_simple_bus_raddr),("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

        for reg in big_regs:
            for i,addr in enumerate(reg):
                self.stim_simple_bus_raddr.append({"data": addr})
                self.ref_simple_bus_rdata.append({"data": good_data[i]})

            # After reading all big registers
            self.cond_simple_bus_wa_wd += [(len(self.stim_simple_bus_wa_wd),("simple_bus_rdata", len(self.ref_simple_bus_rdata)-1))]

            # Overwrite the register content
            for i,addr in enumerate(reg):
                self.stim_simple_bus_wa_wd.append( { 'addr':addr, 'data': bad_data[i] } )

            # After writing to all registers
            self.cond_simple_bus_raddr += [(len(self.stim_simple_bus_raddr),("simple_bus_wa_wd", len(self.stim_simple_bus_wa_wd)-1))]

            # Should read the old good_data, which has been atomically fetched
            for i,addr in enumerate(reg):
                if i > 0: # Avoid new fetching
                    self.stim_simple_bus_raddr.append({"data": addr})
                    self.ref_simple_bus_rdata.append({"data": good_data[i]})

            # Should read the new bad_data, which has been atomically fetched
            for i,addr in enumerate(reg):
                self.stim_simple_bus_raddr.append({"data": addr})
                self.ref_simple_bus_rdata.append({"data": bad_data[i]})

        self.run_it()


    # ----------------------------------------------------------------------------

