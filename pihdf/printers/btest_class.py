from str_builder import StrBuilder
from gtkwave     import print_gtkw_file


def print_btest_file(mfdo):
    '''|
    | Create base test class: t_<module_name>.py file.
    | It also creates 2 .gtkw files used to visualize vcd traces from simulation and co-simulation
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.test_path + '/t_' + mfdo.module_name + ".py"

    s += 'import myhdl\n'
    s += 'import pihdf\n'
    s += 'from pihdf import Testable\n\n'
    s += 'import os, sys\n\n'

    s += 'sys.path.append(os.path.dirname(__file__) + "/../..")\n\n'
    s += 'from ' + mfdo.module_name + '.' + mfdo.module_name + ' import ' + mfdo.module_name + '\n\n'

    s += 'class t_' + mfdo.module_name + '(Testable):\n'
    s += s.indent() + s.header_comment('Automatically generated. Do not modify this file.')

    s += 'pihdf.head("T E S T S")\n'
    s += 'pihdf.info("Using myhdl version " + myhdl.__version__)\n'
    s += 'pihdf.info("Using pihdf version " + pihdf.__version__ + \'\\n\')\n\n'

    s += 'def __init__(self):\n'
    s.indent()

    s += '# call base class constructor\n'
    s += 'Testable.__init__(self)\n\n'

    # test_path used with test_vectors
    s += 'self.test_path = os.path.dirname(__file__)\n\n'

    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        for k in j:
            s += 'self.cond_' + k.inst_name + ' = []\n'
            if k.direction == 0: # IN
                s += 'self.stim_' + k.inst_name + ' = []\n'
            elif k.direction == 1: # OUT
                s += 'self.res_' + k.inst_name + ' = []\n'
    s += 'self.cond_sim_end = {}\n\n'                

    first = True
    pre = ''
    tst_data_str = ''
    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        for k in j:
            pre = '' if first else 26*' '
            tst_data_str += pre + '"cond_' + k.inst_name + '":self.cond_' + k.inst_name + ',\\\n'
            pre = 26*' '
            if k.direction == 0: # IN
                tst_data_str += pre + '"stim_' + k.inst_name + '":self.stim_' + k.inst_name + ',\\\n'
            elif k.direction == 1: # OUT
                tst_data_str += pre + '"res_' + k.inst_name + '":self.res_' + k.inst_name + ',\\\n'
            first = False

    tst_data_str += pre + '"cond_sim_end": self.cond_sim_end'

    s += 'self.tst_data = { ' + tst_data_str  + ' }\n\n'

    ref_data_str = ''
    first = True
    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        for k in j:
            pre = 26*' ' if not first else ''
            if k.direction == 1: # OUT
                first = False
                ref_data_str += pre + '"' + k.inst_name + '":' + '(self.ref_' + k.inst_name + ', self.res_' + k.inst_name + '),\\\n'
                s += 'self.ref_' + k.inst_name + ' = []\n'
    s.newLine()

    s += 'self.ref_data = { ' + ref_data_str[:-3] + ' }\n\n'

    s += s.dedent() + '# Automatically executed BEFORE every test case\n'
    s += 'def setUp(self):\n'
    s += s.indent() + 'print ""\n\n'

    s += s.dedent() + '# Automatically executed AFTER every test case\n'
    s += 'def tearDown(self):\n'
    s += s.indent() + 'print ""\n'
    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        for k in j:
            s += 'self.cond_' + k.inst_name + ' = []\n'
            if k.direction == 0: # IN
                s += 'self.stim_' + k.inst_name + ' = []\n'
            elif k.direction == 1: # OUT
                s += 'self.res_' + k.inst_name + ' = []\n'
                s += 'self.ref_' + k.inst_name + ' = []\n'
    s.newLine()

    s += s.dedent() + '# Data has been previously generated and written to files\n'
    s += 'def use_data_from_files(self):\n'
    s.indent()
    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        for k in j:
            if k.direction == 0: # IN
                s += 'self.stim_' + k.inst_name + '.append({"file" : self.test_path + "/vectors/' + k.inst_name + '.tvr"})\n'
            elif k.direction == 1: # OUT
                s += 'self.res_' + k.inst_name + '.append({"file" : self.test_path + "/vectors/my_' + k.inst_name + '.tvr"})\n'
                s += 'self.ref_' + k.inst_name + '.append({"file" : self.test_path + "/vectors/'    + k.inst_name + '.tvr"})\n'
    s.newLine()
    s += 'self.checkfiles = True\n'
    s += 'self.run_it()\n\n'

    s += s.dedent() + '# Run the simulation and check the results\n'
    s += 'def run_it(self, checkfiles=False):\n'
    s += s.indent() + 'self.check_config("' + mfdo.module_name + '")\n\n'
    s += mfdo.module_name + '_dut = ' + mfdo.module_name + '(IMPL=self.models)\n'
    s += mfdo.module_name + '_dut.' + 'Simulate(tb_config=self.tb_config, tst_data=self.tst_data, verbose=self.verbose'
    if mfdo.parameters != []:
        s += (s.noIndent() + ', dut_params=self.dut_params')
    s += (s.noIndent() + ')\n')

    s += mfdo.module_name + '_dut.clean()\n\n'

    s += 'self.check_results()\n'
    
    s.write(filename, overwrite = mfdo.overwrite)

    print_gtkw_file(mfdo, cosim = False)
    print_gtkw_file(mfdo, cosim = True)
