from myhdl import *
from pihdf import mylog
from pihdf.interfaces.Bus import Bus

import os, sys
import fileinput

class DutFactory(object):
    '''|
    | Returns a simulation instance of a MyHDL function, intended as a DUT in testbench
    | The user selects a simulator: MyHDL, or co-simulation with external HDL simulator, e.g. icarus
    | The user selects whether traces are generated or not
    |________'''

    def __init__(self, cosimulation=False, trace=False):
        '''  '''
        self._simulator = 'icarus' if cosimulation else "myhdl"
        self._trace     =  trace
        self.top_suffix = "_top"

        # Registry of external HDL simulators
        self.sim_reg = {}

        # Register icarus as default external HDL simulator
        self.registerSimulator(
            name         = "icarus",
            hdl          = "Verilog",
            analyze_cmd  = 'iverilog -o {topname}.o -f {modulepath}/src/compile_list.txt',
            simulate_cmd = "vvp -m /.pihdf/myhdl.vpi {topname}.o"
        )

    def registerSimulator(self, name=None, hdl=None, analyze_cmd=None, elaborate_cmd=None, simulate_cmd=None):
        '''|
        | Registers an HDL _simulator
        |        name          - str, user defined name, used to identify this _simulator record
        |        hdl           - str, case insensitive, (verilog, vhdl), the HDL to which the simulated MyHDL code will be converted
        |        analyze_cmd   - str, system command that will be run to analyze the generated HDL
        |        elaborate_cmd - str, optional, system command that will be run after the analyze phase
        |        simulate_cmd  - str, system command that will be run to simulate the analyzed and elaborated design
        |
        |        Before execution of a command string the following substitutions take place:
        |            {topname} is substituted with the name of the simulated MyHDL function
        |________'''
        if not isinstance(name, str) or (name.strip() == ""):
            raise ValueError("Invalid _simulator name")

        if hdl.lower() not in ("vhdl", "verilog"):
            raise ValueError("Invalid hdl {}".format(hdl))

        if not isinstance(analyze_cmd, str) or (analyze_cmd.strip() == ""):
            raise ValueError("Invalid analyzer command")

        if elaborate_cmd is not None:
            if not isinstance(elaborate_cmd, str) or (elaborate_cmd.strip() == ""):
                raise ValueError("Invalid elaborate_cmd command")

        if not isinstance(simulate_cmd, str) or (simulate_cmd.strip() == ""):
            raise ValueError("Invalid _simulator command")

        self.sim_reg[name] = (hdl.lower(), analyze_cmd, elaborate_cmd, simulate_cmd)


    def selectSimulator(self, simulatorName):
        if not simulatorName:
            raise ValueError("No simulator specified")

        if not simulatorName=='myhdl' and not self.sim_reg.has_key(simulatorName):
            raise ValueError("Simulator {} is not registered".format(simulatorName))

        self._simulator = simulatorName


    def enableTrace(self):
        '''|
        | Enables traces (generate a waveform .vcd file)
        |________'''
        self._trace = True


    def disableTrace(self):
        '''|
        | Disables traces
        |________'''
        self._trace = False


    def _getCosimulation(self, module, **kwargs_struct):
        '''|
        | Returns a co-simulation instance of module.
        | Uses the _simulator specified by self._simulator.
        | Enables traces if self._trace is True
        |     module        - MyHDL function to be simulated
        |     kwargs_struct - dict of module structural interface assignments: for signals, interfaces and parameters
        |________'''
        vals = {}
        vals['topname'] = module.get_name() + self.top_suffix
        vals['modulepath'] = module.c_path # absolute path
        hdlsim = self._simulator
        if not hdlsim:
            raise ValueError("No _simulator specified")
        if not self.sim_reg.has_key(hdlsim):
            raise ValueError("Simulator {} is not registered".format(hdlsim))

        hdl, analyze_cmd, elaborate_cmd, simulate_cmd = self.sim_reg[hdlsim]

        # Convert to HDL
        if hdl == "verilog":
            # Filter parameters from kwargs_struct and supply them to convert
            params = {name: kwargs_struct[name] for name in module.get_all_parameters().keys() if name in kwargs_struct.keys()}

            module.convert(hdl=hdl, params=params, verbose=False)
            traceFile = module.c_path + '/' + module.out_path + '/' + "{topname}_cosim".format(**vals)
            if self._trace:
                self._enableTracesVerilog("./tb_{topname}.v".format(**vals), traceFile)
                mylog.infob("Co-simulating... trace will be generated ({}.vcd)".format(traceFile))
            else:
                mylog.infob("Co-simulating... trace will NOT be generated".format(traceFile))

        # TODO: Proper handling of VHDL (some day)
        # elif hdl == "vhdl":
        #     toVHDL(module, **kwargs_struct)

        # Analyze HDL
        os.system(analyze_cmd.format(**vals))

        # Elaborate
        if elaborate_cmd:
            os.system(elaborate_cmd.format(**vals))

        # Copy resets and clocks from the structural interface to flat the interface
        kwargs_flat = {}
        kwargs_flat.update({name : kwargs_struct[name] for name in module.get_all_resets().keys()})
        kwargs_flat.update({name : kwargs_struct[name] for name in module.get_all_clocks().keys()})

        # Flatten structural interfaces and add them to the flat interface
        for name in module.get_all_interfaces().iterkeys():
            kwargs_flat.update(kwargs_struct[name].get_all_signals())

        # Cosimulation
        return Cosimulation(simulate_cmd.format(**vals), **kwargs_flat)


    def _enableTracesVerilog(self, verilogFile, traceFile):
        '''|
        | Enables traces in a Verilog file
        |________'''
        fname, _ = os.path.splitext(traceFile)
        inserted = False
        for _, line in enumerate(fileinput.input(verilogFile, inplace = 1)):
            sys.stdout.write(line)
            if line.startswith("end") and not inserted:
                sys.stdout.write('\n\n')
                sys.stdout.write('initial begin\n')
                sys.stdout.write('    $dumpfile("{}.vcd");\n'.format(fname))
                sys.stdout.write('    $dumpvars(0, dut);\n')
                sys.stdout.write('end\n\n')
                inserted = True


    def getDut(self, module, **kwargs):
        '''|
        | Returns a simulation instance of module.
        | Uses the simulator specified by self._simulator.
        | Enables traces if self._trace is True
        |     module - MyHDL module (function 'gen') to be simulated
        |     kwargs - dict of module interface assignments: for signals and parameters
        |________'''
        if self._simulator=="myhdl":
            if not self._trace:
                sim_dut = module.gen(**kwargs)
                mylog.infob("Simulating... trace will NOT be generated")
            else:
                traceSignals.name = module.get_name() + self.top_suffix
                sim_dut = traceSignals(module.gen, **kwargs)
                mylog.infob("Simulating... trace will be generated ({}.vcd)".format(traceSignals.name))
        else:
            sim_dut = self._getCosimulation(module, **kwargs)

        return sim_dut


    def __call__(self, module, **kwargs):
        return self.getDut(module, **kwargs)
