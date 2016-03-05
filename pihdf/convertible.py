import myhdl
from myhdl import *
from myhdl._instance import _Instantiator
from myhdl._misc import _isGenSeq

from pihdf.interfaces.HSD  import HSD
from pihdf.interfaces.Bus  import Bus
from pihdf.DutFactory import DutFactory
from pihdf.schedulable import Schedulable

from collections import OrderedDict

import mylog

import os
import sys
import shutil
import fileinput
import traceback
import inspect

import time


class Convertible(object):
    '''|
    | Base class for convertible objects
    |________'''
    def __init__(self):

        self.module_name = self.__class__.__name__
        self.is_top = False
        self.top_suffix = "_top"

        self.resets = []
        self.clocks = []
        self.interfaces = []
        self.parameters = []

        self.IN  = 0
        self.OUT = 1

        self.BEH = 0
        self.RTL = 1
        self.VRG = 2

        # Extract the instance name"
        (filename,line_number,function_name,text)=traceback.extract_stack()[-3]
        self.inst_name = text[:text.find('=')].strip()

        # Used to redirect the generated files in a common directory 
        self.c_path        = os.path.dirname(inspect.getfile(self.__class__))
        self.src_path      = 'src'
        self.out_path      = 'out'
        self.test_path     = 'test'
        self.filedump_path = self.c_path  + '/test/vectors/'

        self.fdump = False


    def init_parameters(self, dut_params={}, verbose=True):
        '''|
        | Assign values to parameters. The values are provided from unit tests.
        | If a value for a parameter is not provided, then the default value is used.
        | Default value is always given when creating a Parameter object)
        |________'''
        for def_param in self.get_parameters():
            if def_param.inst_name in dut_params.keys():
                def_param.value = dut_params[def_param.inst_name]
            elif verbose:
                mylog.warn("No initial value provided for parameter '%s'. The default value (%s = %s) will be used." % (def_param, def_param, def_param.value))

    def get_name(self):
        '''|
        | Returns the name of the HW module
        |________'''
        return self.module_name

    def get_resets(self):
        '''|
        | Returns a list of (unique) resets objects
        |________'''
        return self.resets()

    def get_clocks(self):
        '''|
        | Returns a list of (unique) clock objects
        |________'''
        return self.clocks()

    def get_interfaces(self, FDUMP=False):
        '''|
        | Returns a list of (unique) interface objects
        |________'''
        fdump = self.filedump_path if FDUMP else None
        return self.interfaces(fdump)

    def get_parameters(self):
        '''|
        | Returns the list of parameters objects
        |________'''
        return self.parameters # (not defined with lambda)

    def get_parameter_value(self, aParameterName):
        '''|
        | Returns a parameter value given a parameter name
        |________'''
        for i in self.parameters:
            if i.inst_name == aParameterName:
                return i.value


    def get_all_resets(self):
        '''|
        | Returns OrderedDict of all resets (unique)
        |________'''
        return OrderedDict([(rst.inst_name, rst) for rst in self.get_resets()])

    def get_all_clocks(self):
        '''|
        | Returns OrderedDict of all clocks (unique)
        |________'''
        return OrderedDict([(clk.inst_name, clk) for clk in self.get_clocks()])

    def get_all_interfaces(self, FDUMP=False):
        '''|
        | Returns OrderedDict of all interface (unique)
        |________'''
        return OrderedDict([(interface.inst_name, interface) for interface in self.get_interfaces(FDUMP)])

    def get_all_parameters(self, overwrite_params={}, verbose=False):
        '''|
        | Returns OrderedDict of all parameters (unique). Overwrites the parameters given in overwrite_params
        |________'''
        params = OrderedDict([(parameter.inst_name, parameter.value) for parameter in self.get_parameters()])
        for x in params.keys():
            if x in overwrite_params:
                params[x] = overwrite_params[x]
            elif verbose:
                mylog.warn("No initial value provided for parameter '%s'. The default value (%s = %s) will be used." % (x, x, params[x]))
        return params


    def simulationControl(self, tst_data, sim_time, **dut_kwargs):
        '''|
        | Drive values to signals and collect results from simulation
        |________'''
        rst = dut_kwargs[ self.get_resets()[0].inst_name ] # TODO: Works only for 1 reset
        clk = dut_kwargs[ self.get_clocks()[0].inst_name ] # TODO: Works only for 1 clock

        ls_drivers = []
        shed_param = {}
        for interface_name in self.get_all_interfaces().keys():
            interface = dut_kwargs[interface_name] # TODO: check for presence
            enable, done = [Signal(bool(0)) for _ in range(2)]
            ipg = None

            if isinstance(interface, Bus):
                for ii in interface.interfaces():
                    enable, done = [Signal(bool(0)) for _ in range(2)]
                    ls_drivers.append(ii.driver(clk, enable, done, tst_data))
                    ipg = self.ipgi if ii.direction == self.IN else self.ipgo
                    shed_param[ii.inst_name] = (done, enable, ipg)
            else:
                ls_drivers.append(interface.driver(clk, enable, done, tst_data))
                ipg = self.ipgi if interface.direction == self.IN else self.ipgo
                shed_param[interface_name] = (done, enable, ipg)

        sheduler = Schedulable().gen(rst, clk, shed_param, tst_data, sim_time)

        return instances()


    def Testbench(self, tb_config, tst_data, dut_params={}, verbose=False):
        '''|
        | Set-up and run a simulation of a HW module
        | Uses a DutFactory
        |________'''

        self.is_top = True

        # TODO: Dirty patches
        BUS_PATCH = None
        RST_PATCH = None
        CLK_PATCH = None

        trace        = tb_config["trace"]
        cosimulation = tb_config["cosimulation"]
        sim_time     = tb_config["simulation_time"]
        self.ipgi    = tb_config["ipgi"]
        self.ipgo    = tb_config["ipgo"]

        self.fdump = tb_config["fdump"]
        # Used to create test-vector files from behavior top-level model
        FDUMP = self.fdump and self.IMPL == self.BEH

        if len([self.get_interfaces()]) == 0:
            mylog.infob("Nothing to simulate: module contains no interfaces!")
            return

        # Get clocks and instantiate clock generators
        CLK_Period_ns = 1 # clk period = 20ns
        clocks = self.get_all_clocks()
        clk_gen = [clk.gen(CLK_Period_ns) for clk in clocks.values()]
        CLK_PATCH = clocks.values()[-1] # TODO: Dirty patch, keeps the last from the list

        # Get resets and instantiate reset generators
        resets = self.get_all_resets()
        rst_gen = [rst.pulse(CLK_PATCH, 10) for rst in resets.values()]
        RST_PATCH = resets.values()[-1] # TODO: Dirty patch, keeps the last from the list

        # Get interfaces
        interfaces = self.get_all_interfaces(FDUMP)

        # Overwrite default parameters
        parameters = self.get_all_parameters(overwrite_params=dut_params, verbose=True)

        # Add resets, clock, interfaces, and parameter to DUT argument dictionary
        dut_kwargs = {}
        dut_kwargs.update(resets)
        dut_kwargs.update(clocks)
        dut_kwargs.update(interfaces)
        dut_kwargs.update(parameters)


        ## Create DUT factory
        #dutFact = DutFactory()

        ## Configure DUT factory
        #if cosimulation:
            #dutFact.selectSimulator('icarus')
        #else:
            #dutFact.selectSimulator('myhdl')

        #if trace:
            #dutFact.enableTrace()

        # Generate DUT
        #sim_dut = dutFact(self, **dut_kwargs)

        sim_dut = DutFactory(cosimulation, trace).getDut(self, **dut_kwargs)

        sim_control = self.simulationControl(tst_data=tst_data, sim_time=sim_time, **dut_kwargs)

        return instances()


    def Simulate(self, tb_config, tst_data, dut_params={}, verbose=False):
        _start = time.time()

        tb = self.Testbench(tb_config, tst_data, dut_params, verbose)
#         tb = traceSignals(self.Testbench, tb_config, tst_data, dut_params, verbose)
        Simulation(tb).run()

        if verbose:
            mylog.infob("Simulation took %s seconds" % (time.time() - _start))


    def gen(self, **kwargs):
        '''|
        | Function gen(): the top-level implementation method
        |________'''
        if self.IMPL == self.BEH:
            # remove resets from **kwargs
            r_kwargs = dict(kwargs)
            for rst in self.get_resets():
                del r_kwargs[rst.inst_name]

            # remove clocks from **kwargs
            for clk in self.get_clocks():
                del r_kwargs[clk.inst_name]

            logic = []
            clk = kwargs[self.get_clocks()[0].inst_name]

            for x in self.get_interfaces():
                if isinstance(x, Bus):
                    xx = r_kwargs[x.inst_name]
                    for ii in xx.interfaces():
                        if ii.direction == self.IN:
                            logic.append( ii.toListInst( clk ))
                        elif ii.direction == self.OUT:
                            logic.append(ii.fromListInst( clk ))
                        else:
                            raise ValueError
                else:
                    if x.inst_name in r_kwargs:
                        xx = r_kwargs[x.inst_name]
                        # Do not check xx because in case of structural designs,
                        # it does not have direction set (local interface)
                        if x.direction == self.IN: 
                            logic.append( xx.toListInst( clk ))
                        elif x.direction == self.OUT:
                            logic.append(xx.fromListInst( clk ))
                        else:
                            raise ValueError

            @always(clk.posedge)
            def beh_prcs():
                self.funcdict['beh'](**r_kwargs)

            return instances()

        if self.IMPL == self.RTL:
            if self.structural == True:
                FDUMP = self.filedump_path if self.fdump else None
                kwargs.update({"FDUMP":FDUMP, "IMPL":self.models})

            if self.is_top:
                # Instantiate all register files
                rtl = self.funcdict['rtl'](**kwargs)
                ls_rf = []
                rst = kwargs[ self.get_resets()[0].inst_name ] # TODO: Works only for 1 reset
                clk = kwargs[ self.get_clocks()[0].inst_name ] # TODO: Works only for 1 clock
                for name in self.get_all_interfaces().iterkeys():
                    interface = kwargs[name]
                    if isinstance(interface, Bus) and interface.reg_file == True:
                        ls_rf.append(interface.create_reg_file(rst, clk, self.c_path + '/' + self.out_path + '/' + self.module_name + '_mem_map.txt'))
                return instances()

            return self.funcdict['rtl'](**kwargs)


        if self.IMPL == self.VRG:
            kwargs.update({"INST_NAME":self.inst_name})
            return self.funcdict['vrg'](**kwargs)


    def flat2struct(self, **kwargs):
        '''|
        | Adapts flat interface to structural interface
        |________'''

        assign = []

        interfaces = self.get_all_interfaces()

        # Connect top flat signals to interface signals
        for interface in interfaces.itervalues():
            args = [kwargs.get(full_name, None) for full_name in interface.get_all_signals().iterkeys()]
            assign.append(interface.assign(*args))

        # Connect clocks, resets and parameters directly
        gen_kwargs = {}
        gen_kwargs.update(interfaces)
        gen_kwargs.update({ name : kwargs.get(name, None) for name in self.get_all_clocks().keys()})
        gen_kwargs.update({ name : kwargs.get(name, None) for name in self.get_all_resets().keys()})
        gen_kwargs.update({ name : kwargs.get(name, None) for name in self.get_all_parameters().keys()})

        _top = self.gen(**gen_kwargs) # The name _top is detected in the reg_file when hierarchy is extracted

        return instances()


    def convert(self, hdl='verilog', params={}, verbose=True):
        '''|
        | Converts convertible to HDL
        |________'''
        if self.IMPL == self.BEH:
            mylog.err("Behavior models can not be converted to verilog!")
            exit(0)

        self.is_top = True
        # Add resets, clock and overwritten parameters to top interface
        top_kwargs = {}
        top_kwargs.update(self.get_all_clocks())
        top_kwargs.update(self.get_all_resets())
        top_kwargs.update(self.get_all_parameters(params, verbose))

        # Add flatten interface signals to top interface
        for x in self.get_all_interfaces().itervalues():
            top_kwargs.update(x.get_all_signals())

        if verbose: mylog.infob('Converting to {}...'.format(hdl))
        if hdl.lower()=='verilog':
            toVerilog.name = self.get_name() + self.top_suffix
            toVerilog(self.top, **top_kwargs)
        elif hdl.lower()=='vhdl':
            toVHDL.name = self.get_name() + self.top_suffix
            toVHDL(self.top, **top_kwargs)
        else:
            raise ValueError("Unknown HDL: {}".format(hdl))


    def clean(self):
        '''|
        | 'Clean' (moves) generated .v and .vcd files to 'module'/out
        | To be used also when generating test vectors...
        |________'''
        filename = self.module_name + self.top_suffix
        for file in os.listdir('.'):
        
            if os.path.isfile(file):
                if file == filename + '.o':
                    os.remove(file)
                if (file == filename + '.vcd') or (file == filename + '.v') or (file == filename + '.vhd') or (file == 'tb_' + filename + '.v'):
                    shutil.move(file, self.c_path + '/' + self.out_path + '/' + file)


# Static member of class Convertible
Convertible.hsd_object = []

def _isFifoInterface(obj):
    '''|
    | Checks whether a local interface object needs to instantiate a FIFO
    |________'''
    if isinstance(obj, HSD):
        if obj.buf_size > 0:
            return True
    return False

def all_instances(rst, clk):
    '''|
    | Identical to (substitutes) function 'instances() of myhdl._misc'
    | In addition, we add the instances of the 'local' interfaces, which create FIFOs
    |________'''
    f = inspect.currentframe()
    d = inspect.getouterframes(f)[1][0].f_locals
    l = []
    for v in d.values():
        if _isGenSeq(v):
            l.append(v)
        # In addition, we need the FIFO instances, but add them only once
        if _isFifoInterface(v):
            if v not in Convertible.hsd_object:
                l.append(v.gen(rst, clk))
                Convertible.hsd_object.append(v)
    return l
