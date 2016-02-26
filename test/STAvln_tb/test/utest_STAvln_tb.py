import unittest

from myhdl_lib import *

from t_STAvln_tb import t_STAvln_tb

from myhdl_lib.simulation import payload_generator

class Test_STAvln_tb(t_STAvln_tb):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_STAvln_tb.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_STAvln_tb.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_STAvln_tb.tearDown(self)



    # Generate stimuli and reference data
    def useDataSet1(self, N):
        pkt_size = range(1,N+1)
        packets = payload_generator(levels=1, dimensions=pkt_size)
        for i, payload in enumerate(packets):
            self.stim_rx16.append({"payload":payload})
            self.ref_tx16.append({"payload":payload})

        pkt_size = range(1,N+1)
        packets = payload_generator(levels=1, dimensions=pkt_size)
        for payload in packets:
            self.stim_rx32.append({"payload":payload})
            self.ref_tx32.append({"payload":payload})

        pkt_size   = range(1,N+1)
        packets = payload_generator(levels=1, dimensions=pkt_size)
        for payload in packets:
            self.stim_rx64.append({"payload":payload})
            self.ref_tx64.append({"payload":payload})

        self.run_it()

    def setIPG(self, N, VI, VO):
        for i in range(N):
            self.ref_ipg_rx16.append({"data":VI})
            self.ref_ipg_tx16.append({"data":VO})
            
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Pass through, default IPG=0, however, IPG not considered in behavior models """

        self.models = {"top":self.BEH}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":False, "trace":False, "fdump":False}

        self.useDataSet1(3*8)

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Pass through, IPG=1 """

        self.verbose = True
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":390, "cosimulation":False, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        self.setIPG(3*8-1, 1, 1)
        self.useDataSet1(3*8)
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Pass through, IPG=1 """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":220, "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        self.setIPG(3*8-1, 1, 1)
        self.useDataSet1(3*8)
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: Pass through, IPGO=1 """

        IPG = 4
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":320, "cosimulation":True, "trace":False, "fdump":False, "ipgi":IPG, "ipgo":1}

        self.setIPG(3*8-1, 4, 1)
        self.useDataSet1(3*8)
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_005(self):
        """ >>>>>> TEST_005: Pass through """

        IPG = 0
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":True, "trace":False, "fdump":False, "ipgi":IPG, "ipgo":IPG}

        self.setIPG(3*8-1, IPG, IPG)
        self.useDataSet1(3*8)

    # ----------------------------------------------------------------------------
