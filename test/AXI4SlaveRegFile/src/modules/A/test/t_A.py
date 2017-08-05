import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from A.A import A

class t_A(Testable):
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

        self.cond_sbus_waddr = []
        self.stim_sbus_waddr = []
        self.cond_sbus_wdata = []
        self.stim_sbus_wdata = []
        self.cond_sbus_wresp = []
        self.res_sbus_wresp = []
        self.cond_sbus_raddr = []
        self.stim_sbus_raddr = []
        self.cond_sbus_rdata = []
        self.res_sbus_rdata = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_sbus_waddr":self.cond_sbus_waddr,\
                          "stim_sbus_waddr":self.stim_sbus_waddr,\
                          "cond_sbus_wdata":self.cond_sbus_wdata,\
                          "stim_sbus_wdata":self.stim_sbus_wdata,\
                          "cond_sbus_wresp":self.cond_sbus_wresp,\
                          "res_sbus_wresp":self.res_sbus_wresp,\
                          "cond_sbus_raddr":self.cond_sbus_raddr,\
                          "stim_sbus_raddr":self.stim_sbus_raddr,\
                          "cond_sbus_rdata":self.cond_sbus_rdata,\
                          "res_sbus_rdata":self.res_sbus_rdata,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_sbus_wresp = []
        self.ref_sbus_rdata = []

        self.ref_data = { "sbus_wresp":(self.ref_sbus_wresp, self.res_sbus_wresp),\
                          "sbus_rdata":(self.ref_sbus_rdata, self.res_sbus_rdata) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_sbus_waddr = []
        self.stim_sbus_waddr = []
        self.cond_sbus_wdata = []
        self.stim_sbus_wdata = []
        self.cond_sbus_wresp = []
        self.res_sbus_wresp = []
        self.ref_sbus_wresp = []
        self.cond_sbus_raddr = []
        self.stim_sbus_raddr = []
        self.cond_sbus_rdata = []
        self.res_sbus_rdata = []
        self.ref_sbus_rdata = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_sbus_waddr.append({"file" : self.test_path + "/vectors/sbus_waddr.tvr"})
        self.stim_sbus_wdata.append({"file" : self.test_path + "/vectors/sbus_wdata.tvr"})
        self.res_sbus_wresp.append({"file" : self.test_path + "/vectors/my_sbus_wresp.tvr"})
        self.ref_sbus_wresp.append({"file" : self.test_path + "/vectors/sbus_wresp.tvr"})
        self.stim_sbus_raddr.append({"file" : self.test_path + "/vectors/sbus_raddr.tvr"})
        self.res_sbus_rdata.append({"file" : self.test_path + "/vectors/my_sbus_rdata.tvr"})
        self.ref_sbus_rdata.append({"file" : self.test_path + "/vectors/sbus_rdata.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("A")

        A_dut = A(IMPL=self.models)
        A_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        A_dut.clean()

        self.check_results()
