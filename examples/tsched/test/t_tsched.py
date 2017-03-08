import myhdl
import pihdf
from pihdf import Testable
from pihdf import pschedule

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from tsched.tsched import tsched

class t_tsched(Testable):
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

        self.cond_rx_port = []
        self.stim_rx_port = []
        self.cond_tx_port = []
        self.res_tx_port = []
        self.cond_rx = []
        self.stim_rx = []
        self.cond_tx = []
        self.res_tx = []
        self.cond_sim_end = {}

        self.assign_tst_data()

        self.ref_tx_port = []
        self.ref_tx = []

        self.ref_data = { "tx_port":(self.ref_tx_port, self.res_tx_port),\
                          "tx":(self.ref_tx, self.res_tx) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rx_port = []
        self.stim_rx_port = []
        self.cond_tx_port = []
        self.res_tx_port = []
        self.ref_tx_port = []
        self.cond_rx = []
        self.stim_rx = []
        self.cond_tx = []
        self.res_tx = []
        self.ref_tx = []

        pschedule.clear_configurations()

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rx_port.append({"file" : self.test_path + "/vectors/rx_port.tvr"})
        self.res_tx_port.append({"file" : self.test_path + "/vectors/my_tx_port.tvr"})
        self.ref_tx_port.append({"file" : self.test_path + "/vectors/tx_port.tvr"})
        self.stim_rx.append({"file" : self.test_path + "/vectors/rx.tvr"})
        self.res_tx.append({"file" : self.test_path + "/vectors/my_tx.tvr"})
        self.ref_tx.append({"file" : self.test_path + "/vectors/tx.tvr"})

        # TODO: condition lists?

        self.checkfiles = True
        self.run_it()

    def assign_tst_data(self):
        self.tst_data = { "cond_rx_port":self.cond_rx_port,\
                          "stim_rx_port":self.stim_rx_port,\
                          "cond_tx_port":self.cond_tx_port,\
                          "res_tx_port":self.res_tx_port,\
                          "cond_rx":self.cond_rx,\
                          "stim_rx":self.stim_rx,\
                          "cond_tx":self.cond_tx,\
                          "res_tx":self.res_tx,\
                          "cond_sim_end": self.cond_sim_end }

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("tsched")

        self.cond_rx_port = pschedule.get_condition_generator("rx_port")
        self.cond_tx_port = pschedule.get_condition_generator("tx_port")
        self.cond_rx = pschedule.get_condition_generator("rx")
        self.cond_tx = pschedule.get_condition_generator("tx")

        self.assign_tst_data()

        tsched_dut = tsched(IMPL=self.models)
        tsched_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        tsched_dut.clean()

        self.check_results()
