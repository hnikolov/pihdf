import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from STAvln_tb.STAvln_tb import STAvln_tb

class t_STAvln_tb(Testable):
    '''|
    | Automatically generated. Do not modify this file.
    |________'''
    pihdf.head("T E S T S")
    pihdf.info("Using myhdl version " + myhdl.__version__)
    pihdf.info("Using pihdf version " + pihdf.__version__ + '\n')

    def __init__(self):
        # call base class constructor
        Testable.__init__(self)

        self.test_path = os.path.dirname(__file__)

        self.cond_rx16 = []
        self.stim_rx16 = []
        self.cond_tx16 = []
        self.res_tx16 = []
        self.cond_rx32 = []
        self.stim_rx32 = []
        self.cond_tx32 = []
        self.res_tx32 = []
        self.cond_rx64 = []
        self.stim_rx64 = []
        self.cond_tx64 = []
        self.res_tx64 = []
        self.cond_ipg_rx16 = []
        self.res_ipg_rx16 = []
        self.cond_ipg_tx16 = []
        self.res_ipg_tx16 = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_rx16":self.cond_rx16,\
                          "stim_rx16":self.stim_rx16,\
                          "cond_tx16":self.cond_tx16,\
                          "res_tx16":self.res_tx16,\
                          "cond_rx32":self.cond_rx32,\
                          "stim_rx32":self.stim_rx32,\
                          "cond_tx32":self.cond_tx32,\
                          "res_tx32":self.res_tx32,\
                          "cond_rx64":self.cond_rx64,\
                          "stim_rx64":self.stim_rx64,\
                          "cond_tx64":self.cond_tx64,\
                          "res_tx64":self.res_tx64,\
                          "cond_ipg_rx16":self.cond_ipg_rx16,\
                          "res_ipg_rx16":self.res_ipg_rx16,\
                          "cond_ipg_tx16":self.cond_ipg_tx16,\
                          "res_ipg_tx16":self.res_ipg_tx16,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_tx16 = []
        self.ref_tx32 = []
        self.ref_tx64 = []
        self.ref_ipg_rx16 = []
        self.ref_ipg_tx16 = []

        self.ref_data = { "tx16":(self.ref_tx16, self.res_tx16),\
                          "tx32":(self.ref_tx32, self.res_tx32),\
                          "tx64":(self.ref_tx64, self.res_tx64),\
                          "ipg_rx16":(self.ref_ipg_rx16, self.res_ipg_rx16),\
                          "ipg_tx16":(self.ref_ipg_tx16, self.res_ipg_tx16) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rx16 = []
        self.stim_rx16 = []
        self.cond_tx16 = []
        self.res_tx16 = []
        self.ref_tx16 = []
        self.cond_rx32 = []
        self.stim_rx32 = []
        self.cond_tx32 = []
        self.res_tx32 = []
        self.ref_tx32 = []
        self.cond_rx64 = []
        self.stim_rx64 = []
        self.cond_tx64 = []
        self.res_tx64 = []
        self.ref_tx64 = []
        self.cond_ipg_rx16 = []
        self.res_ipg_rx16 = []
        self.ref_ipg_rx16 = []
        self.cond_ipg_tx16 = []
        self.res_ipg_tx16 = []
        self.ref_ipg_tx16 = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rx16.append({"file" : self.test_path + "/vectors/rx16.tvr"})
        self.res_tx16.append({"file" : self.test_path + "/vectors/my_tx16.tvr"})
        self.ref_tx16.append({"file" : self.test_path + "/vectors/tx16.tvr"})
        self.stim_rx32.append({"file" : self.test_path + "/vectors/rx32.tvr"})
        self.res_tx32.append({"file" : self.test_path + "/vectors/my_tx32.tvr"})
        self.ref_tx32.append({"file" : self.test_path + "/vectors/tx32.tvr"})
        self.stim_rx64.append({"file" : self.test_path + "/vectors/rx64.tvr"})
        self.res_tx64.append({"file" : self.test_path + "/vectors/my_tx64.tvr"})
        self.ref_tx64.append({"file" : self.test_path + "/vectors/tx64.tvr"})
        self.res_ipg_rx16.append({"file" : self.test_path + "/vectors/my_ipg_rx16.tvr"})
        self.ref_ipg_rx16.append({"file" : self.test_path + "/vectors/ipg_rx16.tvr"})
        self.res_ipg_tx16.append({"file" : self.test_path + "/vectors/my_ipg_tx16.tvr"})
        self.ref_ipg_tx16.append({"file" : self.test_path + "/vectors/ipg_tx16.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("STAvln_tb")

        STAvln_tb_dut = STAvln_tb(IMPL=self.models)
        STAvln_tb_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        STAvln_tb_dut.clean()

        self.check_results()
