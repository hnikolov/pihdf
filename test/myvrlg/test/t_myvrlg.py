import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from myvrlg.myvrlg import myvrlg

class t_myvrlg(Testable):
    '''|
    | Automatically generated. Do not modify this file.
    |________'''
    pihdf.head("T E S T S")
    pihdf.info("Using MyHDL version " + myhdl.__version__)
    pihdf.info("Using MyFramework version " + pihdf.__version__ + '\n')

    def __init__(self):
        # call base class constructor
        Testable.__init__(self)

        self.test_path = os.path.dirname(__file__)

        self.cond_rx_hs = []
        self.stim_rx_hs = []
        self.cond_tx_hs = []
        self.res_tx_hs = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_rx_hs":self.cond_rx_hs,\
                          "stim_rx_hs":self.stim_rx_hs,\
                          "cond_tx_hs":self.cond_tx_hs,\
                          "res_tx_hs":self.res_tx_hs,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_tx_hs = []

        self.ref_data = { "tx_hs":(self.ref_tx_hs, self.res_tx_hs) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rx_hs = []
        self.stim_rx_hs = []
        self.cond_tx_hs = []
        self.res_tx_hs = []
        self.ref_tx_hs = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rx_hs.append({"file" : self.test_path + "/vectors/rx_hs.tvr"})
        self.res_tx_hs.append({"file" : self.test_path + "/vectors/my_tx_hs.tvr"})
        self.ref_tx_hs.append({"file" : self.test_path + "/vectors/tx_hs.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("myvrlg")

        myvrlg_dut = myvrlg(IMPL=self.models)
        myvrlg_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        myvrlg_dut.clean()

        self.check_results()
