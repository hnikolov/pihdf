import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from hsd_struct.hsd_struct import hsd_struct

class t_hsd_struct(Testable):
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

        self.cond_mode_1 = []
        self.stim_mode_1 = []
        self.cond_mode_2 = []
        self.stim_mode_2 = []
        self.cond_LEDs = []
        self.res_LEDs = []
        self.cond_LED_rdy_en = []
        self.res_LED_rdy_en = []
        self.cond_LED_rdy_buff = []
        self.res_LED_rdy_buff = []
        self.cond_LED_rdy_out = []
        self.res_LED_rdy_out = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_mode_1":self.cond_mode_1,\
                          "stim_mode_1":self.stim_mode_1,\
                          "cond_mode_2":self.cond_mode_2,\
                          "stim_mode_2":self.stim_mode_2,\
                          "cond_LEDs":self.cond_LEDs,\
                          "res_LEDs":self.res_LEDs,\
                          "cond_LED_rdy_en":self.cond_LED_rdy_en,\
                          "res_LED_rdy_en":self.res_LED_rdy_en,\
                          "cond_LED_rdy_buff":self.cond_LED_rdy_buff,\
                          "res_LED_rdy_buff":self.res_LED_rdy_buff,\
                          "cond_LED_rdy_out":self.cond_LED_rdy_out,\
                          "res_LED_rdy_out":self.res_LED_rdy_out,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_LEDs = []
        self.ref_LED_rdy_en = []
        self.ref_LED_rdy_buff = []
        self.ref_LED_rdy_out = []

        self.ref_data = { "LEDs":(self.ref_LEDs, self.res_LEDs),\
                          "LED_rdy_en":(self.ref_LED_rdy_en, self.res_LED_rdy_en),\
                          "LED_rdy_buff":(self.ref_LED_rdy_buff, self.res_LED_rdy_buff),\
                          "LED_rdy_out":(self.ref_LED_rdy_out, self.res_LED_rdy_out) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_mode_1 = []
        self.stim_mode_1 = []
        self.cond_mode_2 = []
        self.stim_mode_2 = []
        self.cond_LEDs = []
        self.res_LEDs = []
        self.ref_LEDs = []
        self.cond_LED_rdy_en = []
        self.res_LED_rdy_en = []
        self.ref_LED_rdy_en = []
        self.cond_LED_rdy_buff = []
        self.res_LED_rdy_buff = []
        self.ref_LED_rdy_buff = []
        self.cond_LED_rdy_out = []
        self.res_LED_rdy_out = []
        self.ref_LED_rdy_out = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_mode_1.append({"file" : self.test_path + "/vectors/mode_1.tvr"})
        self.stim_mode_2.append({"file" : self.test_path + "/vectors/mode_2.tvr"})
        self.res_LEDs.append({"file" : self.test_path + "/vectors/my_LEDs.tvr"})
        self.ref_LEDs.append({"file" : self.test_path + "/vectors/LEDs.tvr"})
        self.res_LED_rdy_en.append({"file" : self.test_path + "/vectors/my_LED_rdy_en.tvr"})
        self.ref_LED_rdy_en.append({"file" : self.test_path + "/vectors/LED_rdy_en.tvr"})
        self.res_LED_rdy_buff.append({"file" : self.test_path + "/vectors/my_LED_rdy_buff.tvr"})
        self.ref_LED_rdy_buff.append({"file" : self.test_path + "/vectors/LED_rdy_buff.tvr"})
        self.res_LED_rdy_out.append({"file" : self.test_path + "/vectors/my_LED_rdy_out.tvr"})
        self.ref_LED_rdy_out.append({"file" : self.test_path + "/vectors/LED_rdy_out.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("hsd_struct")

        hsd_struct_dut = hsd_struct(IMPL=self.models)
        hsd_struct_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose, dut_params=self.dut_params)
        hsd_struct_dut.clean()

        self.check_results()
