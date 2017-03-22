import myhdl
import pihdf
from pihdf import Testable

import os, sys

sys.path.append(os.path.dirname(__file__) + "/../..")

from SimpleBusRegFile.SimpleBusRegFile import SimpleBusRegFile

class t_SimpleBusRegFile(Testable):
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

        self.cond_simple_bus_wa_wd = []
        self.stim_simple_bus_wa_wd = []
        self.cond_simple_bus_raddr = []
        self.stim_simple_bus_raddr = []
        self.cond_simple_bus_rdata = []
        self.res_simple_bus_rdata = []
        self.cond_sim_end = {}

        self.tst_data = { "cond_simple_bus_wa_wd":self.cond_simple_bus_wa_wd,\
                          "stim_simple_bus_wa_wd":self.stim_simple_bus_wa_wd,\
                          "cond_simple_bus_raddr":self.cond_simple_bus_raddr,\
                          "stim_simple_bus_raddr":self.stim_simple_bus_raddr,\
                          "cond_simple_bus_rdata":self.cond_simple_bus_rdata,\
                          "res_simple_bus_rdata":self.res_simple_bus_rdata,\
                          "cond_sim_end": self.cond_sim_end }

        self.ref_simple_bus_rdata = []

        self.ref_data = { "simple_bus_rdata":(self.ref_simple_bus_rdata, self.res_simple_bus_rdata) }

    # Automatically executed BEFORE every test case
    def setUp(self):
        print ""

    # Automatically executed AFTER every test case
    def tearDown(self):
        print ""
        self.cond_simple_bus_wa_wd = []
        self.stim_simple_bus_wa_wd = []
        self.cond_simple_bus_raddr = []
        self.stim_simple_bus_raddr = []
        self.cond_simple_bus_rdata = []
        self.res_simple_bus_rdata = []
        self.ref_simple_bus_rdata = []

    # Data has been previously generated and written to files
    def use_data_from_files(self):
        self.stim_simple_bus_wa_wd.append({"file" : self.test_path + "/vectors/simple_bus_wa_wd.tvr"})
        self.stim_simple_bus_raddr.append({"file" : self.test_path + "/vectors/simple_bus_raddr.tvr"})
        self.res_simple_bus_rdata.append({"file" : self.test_path + "/vectors/my_simple_bus_rdata.tvr"})
        self.ref_simple_bus_rdata.append({"file" : self.test_path + "/vectors/simple_bus_rdata.tvr"})

        self.checkfiles = True
        self.run_it()

    # Run the simulation and check the results
    def run_it(self, checkfiles=False):
        self.check_config("SimpleBusRegFile")

        SimpleBusRegFile_dut = SimpleBusRegFile(IMPL=self.models)
        SimpleBusRegFile_dut.Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose)
        SimpleBusRegFile_dut.clean()

        self.check_results()
