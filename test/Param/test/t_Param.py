import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from Param.Param import Param

class t_Param(Testable):
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

        self.cond_tx = []
        self.res_tx = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_tx":self.cond_tx,\
                          "res_tx":self.res_tx,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_tx = []

        self.ref_data = { "tx":(self.ref_tx, self.res_tx) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_tx = []
        self.res_tx = []
        self.ref_tx = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.res_tx.append({"file" : self.test_path + "/vectors/my_tx.tvr"})
        self.ref_tx.append({"file" : self.test_path + "/vectors/tx.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("Param")

        Param_dut = Param(IMPL=self.models)
        Param_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose, dut_params=self.dut_params)
        Param_dut.clean()

        self.check_results()
