import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from TIncr.TIncr import TIncr

class t_TIncr(Testable):
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

        self.cond_mode = []
        self.stim_mode = []
        self.cond_inc_out = []
        self.res_inc_out = []
        self.cond_rdy_en = []
        self.res_rdy_en = []
        self.cond_rdy_buff = []
        self.res_rdy_buff = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_mode":self.cond_mode,\
                          "stim_mode":self.stim_mode,\
                          "cond_inc_out":self.cond_inc_out,\
                          "res_inc_out":self.res_inc_out,\
                          "cond_rdy_en":self.cond_rdy_en,\
                          "res_rdy_en":self.res_rdy_en,\
                          "cond_rdy_buff":self.cond_rdy_buff,\
                          "res_rdy_buff":self.res_rdy_buff,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_inc_out = []
        self.ref_rdy_en = []
        self.ref_rdy_buff = []

        self.ref_data = { "inc_out":(self.ref_inc_out, self.res_inc_out),\
                          "rdy_en":(self.ref_rdy_en, self.res_rdy_en),\
                          "rdy_buff":(self.ref_rdy_buff, self.res_rdy_buff) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_mode = []
        self.stim_mode = []
        self.cond_inc_out = []
        self.res_inc_out = []
        self.ref_inc_out = []
        self.cond_rdy_en = []
        self.res_rdy_en = []
        self.ref_rdy_en = []
        self.cond_rdy_buff = []
        self.res_rdy_buff = []
        self.ref_rdy_buff = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_mode.append({"file" : self.test_path + "/vectors/mode.tvr"})
        self.res_inc_out.append({"file" : self.test_path + "/vectors/my_inc_out.tvr"})
        self.ref_inc_out.append({"file" : self.test_path + "/vectors/inc_out.tvr"})
        self.res_rdy_en.append({"file" : self.test_path + "/vectors/my_rdy_en.tvr"})
        self.ref_rdy_en.append({"file" : self.test_path + "/vectors/rdy_en.tvr"})
        self.res_rdy_buff.append({"file" : self.test_path + "/vectors/my_rdy_buff.tvr"})
        self.ref_rdy_buff.append({"file" : self.test_path + "/vectors/rdy_buff.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("TIncr")

        TIncr_dut = TIncr(IMPL=self.models)
        TIncr_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose, dut_params=self.dut_params)
        TIncr_dut.clean()

        self.check_results()
