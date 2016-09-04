import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from TOut.TOut import TOut

class t_TOut(Testable):
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
        self.cond_inc_in = []
        self.stim_inc_in = []
        self.cond_LEDs = []
        self.res_LEDs = []
        self.cond_rdy_out = []
        self.res_rdy_out = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_mode":self.cond_mode,\
                          "stim_mode":self.stim_mode,\
                          "cond_inc_in":self.cond_inc_in,\
                          "stim_inc_in":self.stim_inc_in,\
                          "cond_LEDs":self.cond_LEDs,\
                          "res_LEDs":self.res_LEDs,\
                          "cond_rdy_out":self.cond_rdy_out,\
                          "res_rdy_out":self.res_rdy_out,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_LEDs = []
        self.ref_rdy_out = []

        self.ref_data = { "LEDs":(self.ref_LEDs, self.res_LEDs),\
                          "rdy_out":(self.ref_rdy_out, self.res_rdy_out) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_mode = []
        self.stim_mode = []
        self.cond_inc_in = []
        self.stim_inc_in = []
        self.cond_LEDs = []
        self.res_LEDs = []
        self.ref_LEDs = []
        self.cond_rdy_out = []
        self.res_rdy_out = []
        self.ref_rdy_out = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_mode.append({"file" : self.test_path + "/vectors/mode.tvr"})
        self.stim_inc_in.append({"file" : self.test_path + "/vectors/inc_in.tvr"})
        self.res_LEDs.append({"file" : self.test_path + "/vectors/my_LEDs.tvr"})
        self.ref_LEDs.append({"file" : self.test_path + "/vectors/LEDs.tvr"})
        self.res_rdy_out.append({"file" : self.test_path + "/vectors/my_rdy_out.tvr"})
        self.ref_rdy_out.append({"file" : self.test_path + "/vectors/rdy_out.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("TOut")

        TOut_dut = TOut(IMPL=self.models)
        TOut_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        TOut_dut.clean()

        self.check_results()
