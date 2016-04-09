import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from hsd_custom.hsd_custom import hsd_custom

class t_hsd_custom(Testable):
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

        self.cond_rx_port_flds = []
        self.stim_rx_port_flds = []
        self.cond_tx_port_flds = []
        self.res_tx_port_flds = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_rx_port_flds":self.cond_rx_port_flds,\
                          "stim_rx_port_flds":self.stim_rx_port_flds,\
                          "cond_tx_port_flds":self.cond_tx_port_flds,\
                          "res_tx_port_flds":self.res_tx_port_flds,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_tx_port_flds = []

        self.ref_data = { "tx_port_flds":(self.ref_tx_port_flds, self.res_tx_port_flds) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rx_port_flds = []
        self.stim_rx_port_flds = []
        self.cond_tx_port_flds = []
        self.res_tx_port_flds = []
        self.ref_tx_port_flds = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rx_port_flds.append({"file" : self.test_path + "/vectors/rx_port_flds.tvr"})
        self.res_tx_port_flds.append({"file" : self.test_path + "/vectors/my_tx_port_flds.tvr"})
        self.ref_tx_port_flds.append({"file" : self.test_path + "/vectors/tx_port_flds.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("hsd_custom")

        hsd_custom_dut = hsd_custom(IMPL=self.models)
        hsd_custom_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        hsd_custom_dut.clean()

        self.check_results()
