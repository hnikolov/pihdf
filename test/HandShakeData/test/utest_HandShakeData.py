import unittest

from myhdl_lib import *

from t_HandShakeData import t_HandShakeData


class Test_HandShakeData(t_HandShakeData):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_HandShakeData.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_HandShakeData.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_HandShakeData.tearDown(self)


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_001(self):
        """ >>>>>> TEST_001: Handshake(width) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":300, "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_width.append({"data":i})
            self.ref_tx_width.append({"data":i})
            self.ref_ipg_rx_width.append({"data":1})
            self.ref_ipg_tx_width.append({"data":1})

        self.ref_ipg_rx_width.pop(-1)
        self.ref_ipg_tx_width.pop(-1)

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Handshake(fields) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            bit = i%3 == 0
            byte = i%256
            word = i + 800
            self.stim_rx_fields.append({"bit":bit, "byte":byte, "word":word})
            self.ref_tx_fields.append({"bit":bit, "byte":byte, "word":word})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Handshake(width, buf) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_width_buf.append({"data":i})
            self.ref_tx_width_buf.append({"data":i})

        print "Testing the presence of buffer space. Simulation should not deadlock."

        # Start capturing after the first 6 stimuli words are accepted (4 words fifo + 2 pipe stages)
        # BUF_DEPTH = 4
        self.cond_tx_width_buf.append((0, ("rx_width_buf", 6-1)))

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: Handshake(fields, buf) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            bit = i%3 == 0
            byte = i%256
            word = i + 800
            self.stim_rx_fields_buf.append({"bit":bit, "byte":byte, "word":word})
            self.ref_tx_fields_buf.append({"bit":bit, "byte":byte, "word":word})

        print "Testing the presence of buffer space. Simulation should not deadlock."

        #Start capturing after the first 6 stimuli words are accepted (4 words fifo + 2 pipe stages)
        BUF_DEPTH = 4
        self.cond_tx_fields_buf.append((0, ("rx_fields_buf", 6-1)))

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_005(self):
        """ >>>>>> TEST_005: Handshake(width) with terminated snk """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            # Should not block, because terminated snk drains data
            self.stim_rx_terminate.append({"data":i})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_006(self):
        """ >>>>>> TEST_006: Handshake(width) with terminated src"""

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            # Should not block because terminated src does not produce data
#             self.ref_tx_terminate.append({"data":i})
            pass

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_007(self):
        """ >>>>>> TEST_007: Handshake(width, push) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_push.append({"data":0x55})

        # The RTL design expects to receive only values of 0x55. 
        # All stimuli should be transmitted although the RTL does not drive the ready signal

        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("Not implemented yet in the HandShake interface")
    def test_008(self):
        """ >>>>>> TEST_008: Handshake(width, pull) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":200, "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(0, 10):
            self.ref_tx_pull.append({"data":i})

        # The RTL design generates a sequence 0,1,2..., as the value is incremented after every read
        # All expected data should be received although the RTL does not drive the valid signal

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_009(self):
        """ >>>>>> TEST_009: Handshake(width) with IPGI """

        IPGI = 5
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":IPGI, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_width.append({"data":i})
            self.ref_tx_width.append({"data":i})
            self.ref_ipg_rx_width.append({"data":IPGI})
            self.ref_ipg_tx_width.append({"data":1})

        self.ref_ipg_rx_width.pop(-1)
        self.ref_ipg_tx_width.pop(-1)

        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("IPGO affects ipg_rx_width and ipg_tx_width, but they does not respect the ready signal. FIXME")
    def test_010(self):
        """ >>>>>> TEST_010: Handshake(width) with IPGO"""

        IPGO = 6
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":IPGO}

        for i in range(100, 110):
            self.stim_rx_width.append({"data":i})
            self.ref_tx_width.append({"data":i})
            self.ref_ipg_rx_width.append({"data":1})
            self.ref_ipg_tx_width.append({"data":IPGO})

        self.ref_ipg_rx_width.pop(-1)
        self.ref_ipg_tx_width.pop(-1)

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_011(self):
        """ >>>>>> TEST_011: Handshake(fields) with negative values """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            bit = i%3 == 0
            byte = -(i%128)
            word = i + 800
            self.stim_rx_fields.append({"bit":bit, "byte":byte, "word":word})
            self.ref_tx_fields.append({"bit":bit, "byte":byte, "word":word})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_012(self):
        """ >>>>>> TEST_012: Handshake(fields, buf) with negative values """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            bit = i%3 == 0
            byte = -(i%128)
            word = i + 800
            self.stim_rx_fields_buf.append({"bit":bit, "byte":byte, "word":word})
            self.ref_tx_fields_buf.append({"bit":bit, "byte":byte, "word":word})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_013(self):
        """ >>>>>> TEST_013: Handshake(fields) assigned with constants """

        # NOTE: MyHDL version 0.8.1 - issue with cosimulation:
        # When signals assigned in always_comb section to constants are propagated from cosimulation to python, 
        # in python we see the signal init value, not the assigned value

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_fields_const.append({"bit":1, "byte":2, "word":3}) # These values are ignored by the RTL
            self.ref_tx_fields_const.append({"bit":1, "byte":-10, "word":0x55AA}) # These values are generated by the RTL


        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_014(self):
        """ >>>>>> TEST_014: Handshake(width, buf) using the Scheduler to control Driver and Capture"""

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        buf_size = 6 # (4 words fifo + 2 pipe stages)
        data_in = data_out = 0

        # Writing rx_width_buf and reading tx_width_buf are interleaved

        for _ in range(10):

            # Write to rx_width_buf only after all data buffered in the design are read from tx_width_buf
            self.cond_rx_width_buf.append((len(self.stim_rx_width_buf),("tx_width_buf", len(self.ref_tx_width_buf)-1)))

            for _ in range(buf_size):
                self.stim_rx_width_buf.append({"data":data_in})
                data_in += 1

            # Read from tx_width_buf only after data is written to rx_width_buf to fill the design buffer
            self.cond_tx_width_buf.append((len(self.ref_tx_width_buf), ("rx_width_buf", len(self.stim_rx_width_buf)-1)))

            for _ in range(buf_size):
                self.ref_tx_width_buf.append({"data":data_out})
                data_out += 1

        print "Testing the presence of buffer space. Simulation should not deadlock."


        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_015(self):
        """ >>>>>> TEST_015: Handshake(width1) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":300, "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_width1.append({"data":i%2})
            self.ref_tx_width1.append({"data":i%2})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_016(self):
        """ >>>>>> TEST_016: Handshake(width1, buf) """

        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":True, "trace":False, "fdump":False, "ipgi":1, "ipgo":1}

        for i in range(100, 200):
            self.stim_rx_width1_buf.append({"data":i%2})
            self.ref_tx_width1_buf.append({"data":i%2})

        print "Testing the presence of buffer space. Simulation should not deadlock."

        # Start capturing after the first 6 stimuli words are accepted (4 words fifo + 2 pipe stages)
        # BUF_DEPTH = 4
        self.cond_tx_width_buf.append((0, ("rx_width_buf", 6-1)))

        self.run_it()


    # ----------------------------------------------------------------------------
