import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from B.B import B

class t_B(Testable):
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

        self.cond_sbus_wa_wd = []
        self.stim_sbus_wa_wd = []
        self.cond_sbus_raddr = []
        self.stim_sbus_raddr = []
        self.cond_sbus_rdata = []
        self.res_sbus_rdata = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_sbus_wa_wd":self.cond_sbus_wa_wd,\
                          "stim_sbus_wa_wd":self.stim_sbus_wa_wd,\
                          "cond_sbus_raddr":self.cond_sbus_raddr,\
                          "stim_sbus_raddr":self.stim_sbus_raddr,\
                          "cond_sbus_rdata":self.cond_sbus_rdata,\
                          "res_sbus_rdata":self.res_sbus_rdata,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_sbus_rdata = []

        self.ref_data = { "sbus_rdata":(self.ref_sbus_rdata, self.res_sbus_rdata) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_sbus_wa_wd = []
        self.stim_sbus_wa_wd = []
        self.cond_sbus_raddr = []
        self.stim_sbus_raddr = []
        self.cond_sbus_rdata = []
        self.res_sbus_rdata = []
        self.ref_sbus_rdata = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_sbus_wa_wd.append({"file" : self.test_path + "/vectors/sbus_wa_wd.tvr"})
        self.stim_sbus_raddr.append({"file" : self.test_path + "/vectors/sbus_raddr.tvr"})
        self.res_sbus_rdata.append({"file" : self.test_path + "/vectors/my_sbus_rdata.tvr"})
        self.ref_sbus_rdata.append({"file" : self.test_path + "/vectors/sbus_rdata.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("B")

        B_dut = B(IMPL=self.models)
        B_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        B_dut.clean()

        self.check_results()
