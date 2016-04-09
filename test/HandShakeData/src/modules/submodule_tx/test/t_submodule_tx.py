import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from submodule_tx.submodule_tx import submodule_tx

class t_submodule_tx(Testable):
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

        self.cond_rx_width = []
        self.stim_rx_width = []
        self.cond_tx_width = []
        self.res_tx_width = []
        self.cond_rx_width1 = []
        self.stim_rx_width1 = []
        self.cond_tx_width1 = []
        self.res_tx_width1 = []
        self.cond_rx_fields = []
        self.stim_rx_fields = []
        self.cond_tx_fields = []
        self.res_tx_fields = []
        self.cond_rx_width_buf = []
        self.stim_rx_width_buf = []
        self.cond_tx_width_buf = []
        self.res_tx_width_buf = []
        self.cond_rx_width1_buf = []
        self.stim_rx_width1_buf = []
        self.cond_tx_width1_buf = []
        self.res_tx_width1_buf = []
        self.cond_rx_fields_buf = []
        self.stim_rx_fields_buf = []
        self.cond_tx_fields_buf = []
        self.res_tx_fields_buf = []
        self.cond_rx_fields_const = []
        self.stim_rx_fields_const = []
        self.cond_tx_fields_const = []
        self.res_tx_fields_const = []
        self.cond_tx_pull = []
        self.res_tx_pull = []
        self.cond_rx_terminate = []
        self.stim_rx_terminate = []
        self.cond_tx_terminate = []
        self.res_tx_terminate = []
        self.cond_ipg_tx_width = []
        self.res_ipg_tx_width = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_rx_width":self.cond_rx_width,\
                          "stim_rx_width":self.stim_rx_width,\
                          "cond_tx_width":self.cond_tx_width,\
                          "res_tx_width":self.res_tx_width,\
                          "cond_rx_width1":self.cond_rx_width1,\
                          "stim_rx_width1":self.stim_rx_width1,\
                          "cond_tx_width1":self.cond_tx_width1,\
                          "res_tx_width1":self.res_tx_width1,\
                          "cond_rx_fields":self.cond_rx_fields,\
                          "stim_rx_fields":self.stim_rx_fields,\
                          "cond_tx_fields":self.cond_tx_fields,\
                          "res_tx_fields":self.res_tx_fields,\
                          "cond_rx_width_buf":self.cond_rx_width_buf,\
                          "stim_rx_width_buf":self.stim_rx_width_buf,\
                          "cond_tx_width_buf":self.cond_tx_width_buf,\
                          "res_tx_width_buf":self.res_tx_width_buf,\
                          "cond_rx_width1_buf":self.cond_rx_width1_buf,\
                          "stim_rx_width1_buf":self.stim_rx_width1_buf,\
                          "cond_tx_width1_buf":self.cond_tx_width1_buf,\
                          "res_tx_width1_buf":self.res_tx_width1_buf,\
                          "cond_rx_fields_buf":self.cond_rx_fields_buf,\
                          "stim_rx_fields_buf":self.stim_rx_fields_buf,\
                          "cond_tx_fields_buf":self.cond_tx_fields_buf,\
                          "res_tx_fields_buf":self.res_tx_fields_buf,\
                          "cond_rx_fields_const":self.cond_rx_fields_const,\
                          "stim_rx_fields_const":self.stim_rx_fields_const,\
                          "cond_tx_fields_const":self.cond_tx_fields_const,\
                          "res_tx_fields_const":self.res_tx_fields_const,\
                          "cond_tx_pull":self.cond_tx_pull,\
                          "res_tx_pull":self.res_tx_pull,\
                          "cond_rx_terminate":self.cond_rx_terminate,\
                          "stim_rx_terminate":self.stim_rx_terminate,\
                          "cond_tx_terminate":self.cond_tx_terminate,\
                          "res_tx_terminate":self.res_tx_terminate,\
                          "cond_ipg_tx_width":self.cond_ipg_tx_width,\
                          "res_ipg_tx_width":self.res_ipg_tx_width,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_tx_width = []
        self.ref_tx_width1 = []
        self.ref_tx_fields = []
        self.ref_tx_width_buf = []
        self.ref_tx_width1_buf = []
        self.ref_tx_fields_buf = []
        self.ref_tx_fields_const = []
        self.ref_tx_pull = []
        self.ref_tx_terminate = []
        self.ref_ipg_tx_width = []

        self.ref_data = { "tx_width":(self.ref_tx_width, self.res_tx_width),\
                          "tx_width1":(self.ref_tx_width1, self.res_tx_width1),\
                          "tx_fields":(self.ref_tx_fields, self.res_tx_fields),\
                          "tx_width_buf":(self.ref_tx_width_buf, self.res_tx_width_buf),\
                          "tx_width1_buf":(self.ref_tx_width1_buf, self.res_tx_width1_buf),\
                          "tx_fields_buf":(self.ref_tx_fields_buf, self.res_tx_fields_buf),\
                          "tx_fields_const":(self.ref_tx_fields_const, self.res_tx_fields_const),\
                          "tx_pull":(self.ref_tx_pull, self.res_tx_pull),\
                          "tx_terminate":(self.ref_tx_terminate, self.res_tx_terminate),\
                          "ipg_tx_width":(self.ref_ipg_tx_width, self.res_ipg_tx_width) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_rx_width = []
        self.stim_rx_width = []
        self.cond_tx_width = []
        self.res_tx_width = []
        self.ref_tx_width = []
        self.cond_rx_width1 = []
        self.stim_rx_width1 = []
        self.cond_tx_width1 = []
        self.res_tx_width1 = []
        self.ref_tx_width1 = []
        self.cond_rx_fields = []
        self.stim_rx_fields = []
        self.cond_tx_fields = []
        self.res_tx_fields = []
        self.ref_tx_fields = []
        self.cond_rx_width_buf = []
        self.stim_rx_width_buf = []
        self.cond_tx_width_buf = []
        self.res_tx_width_buf = []
        self.ref_tx_width_buf = []
        self.cond_rx_width1_buf = []
        self.stim_rx_width1_buf = []
        self.cond_tx_width1_buf = []
        self.res_tx_width1_buf = []
        self.ref_tx_width1_buf = []
        self.cond_rx_fields_buf = []
        self.stim_rx_fields_buf = []
        self.cond_tx_fields_buf = []
        self.res_tx_fields_buf = []
        self.ref_tx_fields_buf = []
        self.cond_rx_fields_const = []
        self.stim_rx_fields_const = []
        self.cond_tx_fields_const = []
        self.res_tx_fields_const = []
        self.ref_tx_fields_const = []
        self.cond_tx_pull = []
        self.res_tx_pull = []
        self.ref_tx_pull = []
        self.cond_rx_terminate = []
        self.stim_rx_terminate = []
        self.cond_tx_terminate = []
        self.res_tx_terminate = []
        self.ref_tx_terminate = []
        self.cond_ipg_tx_width = []
        self.res_ipg_tx_width = []
        self.ref_ipg_tx_width = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_rx_width.append({"file" : self.test_path + "/vectors/rx_width.tvr"})
        self.res_tx_width.append({"file" : self.test_path + "/vectors/my_tx_width.tvr"})
        self.ref_tx_width.append({"file" : self.test_path + "/vectors/tx_width.tvr"})
        self.stim_rx_width1.append({"file" : self.test_path + "/vectors/rx_width1.tvr"})
        self.res_tx_width1.append({"file" : self.test_path + "/vectors/my_tx_width1.tvr"})
        self.ref_tx_width1.append({"file" : self.test_path + "/vectors/tx_width1.tvr"})
        self.stim_rx_fields.append({"file" : self.test_path + "/vectors/rx_fields.tvr"})
        self.res_tx_fields.append({"file" : self.test_path + "/vectors/my_tx_fields.tvr"})
        self.ref_tx_fields.append({"file" : self.test_path + "/vectors/tx_fields.tvr"})
        self.stim_rx_width_buf.append({"file" : self.test_path + "/vectors/rx_width_buf.tvr"})
        self.res_tx_width_buf.append({"file" : self.test_path + "/vectors/my_tx_width_buf.tvr"})
        self.ref_tx_width_buf.append({"file" : self.test_path + "/vectors/tx_width_buf.tvr"})
        self.stim_rx_width1_buf.append({"file" : self.test_path + "/vectors/rx_width1_buf.tvr"})
        self.res_tx_width1_buf.append({"file" : self.test_path + "/vectors/my_tx_width1_buf.tvr"})
        self.ref_tx_width1_buf.append({"file" : self.test_path + "/vectors/tx_width1_buf.tvr"})
        self.stim_rx_fields_buf.append({"file" : self.test_path + "/vectors/rx_fields_buf.tvr"})
        self.res_tx_fields_buf.append({"file" : self.test_path + "/vectors/my_tx_fields_buf.tvr"})
        self.ref_tx_fields_buf.append({"file" : self.test_path + "/vectors/tx_fields_buf.tvr"})
        self.stim_rx_fields_const.append({"file" : self.test_path + "/vectors/rx_fields_const.tvr"})
        self.res_tx_fields_const.append({"file" : self.test_path + "/vectors/my_tx_fields_const.tvr"})
        self.ref_tx_fields_const.append({"file" : self.test_path + "/vectors/tx_fields_const.tvr"})
        self.res_tx_pull.append({"file" : self.test_path + "/vectors/my_tx_pull.tvr"})
        self.ref_tx_pull.append({"file" : self.test_path + "/vectors/tx_pull.tvr"})
        self.stim_rx_terminate.append({"file" : self.test_path + "/vectors/rx_terminate.tvr"})
        self.res_tx_terminate.append({"file" : self.test_path + "/vectors/my_tx_terminate.tvr"})
        self.ref_tx_terminate.append({"file" : self.test_path + "/vectors/tx_terminate.tvr"})
        self.res_ipg_tx_width.append({"file" : self.test_path + "/vectors/my_ipg_tx_width.tvr"})
        self.ref_ipg_tx_width.append({"file" : self.test_path + "/vectors/ipg_tx_width.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("submodule_tx")

        submodule_tx_dut = submodule_tx(IMPL=self.models)
        submodule_tx_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        submodule_tx_dut.clean()

        self.check_results()
