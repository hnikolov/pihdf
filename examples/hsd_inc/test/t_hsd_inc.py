import myhdl
import pihdf
from pihdf import Testable
from pihdf import pschedule

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from hsd_inc.hsd_inc import hsd_inc

class t_hsd_inc(Testable):
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

        self.cond_rxd = []
        self.stim_rxd = []
        self.cond_txd = []
        self.res_txd = []
        self.cond_sim_end = {}

        self.assign_tst_data()

        self.ref_txd = []

        self.ref_data = { "txd":(self.ref_txd, self.res_txd) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rxd = []
        self.stim_rxd = []
        self.cond_txd = []
        self.res_txd = []
        self.ref_txd = []

        pschedule.clear_configurations()

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rxd.append({"file" : self.test_path + "/vectors/rxd.tvr"})
        self.res_txd.append({"file" : self.test_path + "/vectors/my_txd.tvr"})
        self.ref_txd.append({"file" : self.test_path + "/vectors/txd.tvr"})

        # TODO: condition lists?

        self.checkfiles = True
        self.run_it()

    def assign_tst_data(self):
        self.tst_data = { "cond_rxd":self.cond_rxd,\
                          "stim_rxd":self.stim_rxd,\
                          "cond_txd":self.cond_txd,\
                          "res_txd":self.res_txd,\
                          "cond_sim_end": self.cond_sim_end }

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("hsd_inc")

        self.cond_rxd = pschedule.get_condition_generator("rxd")
        self.cond_txd = pschedule.get_condition_generator("txd")

        self.assign_tst_data()

        hsd_inc_dut = hsd_inc(IMPL=self.models)
        hsd_inc_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        hsd_inc_dut.clean()

        self.check_results()
