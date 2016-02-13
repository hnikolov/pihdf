from str_builder import StrBuilder


def print_utest_file(mfdo):
    '''|
    | Create utest_<module_name>.py file
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.test_path + '/utest_' + mfdo.module_name + ".py"
    base_test = 't_' + mfdo.module_name
    s += 'import unittest\n\n'
    s += 'from myhdl_lib import *\n\n'

    s += 'from ' + base_test + ' import ' + base_test + '\n\n'

    s += 'class Test_' + mfdo.module_name + '(' + base_test + '):\n'
    s += s.indent() + s.header_comment('The main class for unit-testing. Add your tests here.')

    s += 'def __init__(self):\n'
    s.indent()

    s += '# call base class constructor\n'
    s += base_test + '.__init__(self)\n\n'

    s += s.dedent() + '# Automatically executed BEFORE every TestCase\n'
    s += 'def setUp(self):\n'
    s += s.indent() + base_test + '.setUp(self)\n\n'

    s += s.dedent() + '# Automatically executed AFTER every TestCase\n'
    s += 'def tearDown(self):\n'
    s += s.indent() + base_test + '.tearDown(self)\n\n\n'

    s += s.dedent() + '# ----------------------------------------------------------------------------\n'
    s += '# @unittest.skip("")\n'
    s += 'def test_000(self):\n'
    s += s.indent() + '""" >>>>>> TEST_000: TO DO: describe the test """\n\n'

    if mfdo.parameters != []:
        s += 'self.dut_params = {'
        for p in mfdo.parameters:
            s += (s.noIndent() + '"' + p["name"] + '":' + p["value"] + ', ')
        s = s-2 + (s.noIndent() + '}\n')

    s += 'self.models = {"top":self.BEH}\n'
    s += '# Set fdump to True in order to generate test vector files for the global interfaces\n'
    s += 'self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}\n\n'

    s += '# TO DO: generate stimuli and reference data here\n\n'
    s + 'self.run_it()\n\n'

    # Commented due to problems in case of structured design using BUS interfaces
    #if mfdo.modules != []:
        #s += s.dedent() + '# ----------------------------------------------------------------------------\n'
        #s += '@unittest.skip("")\n'
        #s += 'def test_0000(self):\n'
        #s += s.indent() + '""" >>>>>> TEST_0000: Test template for using stimuli files """\n\n'

        #if mfdo.parameters != []:
            #s += 'self.dut_params = {'
            #for p in mfdo.parameters:
                #s += (s.noIndent() + '"' + p["name"] + '":' + p["value"] + ', ')
            #s = s-2 + (s.noIndent() + '}\n')

        #s += 'self.models = {"top":self.RTL'
        #for m in mfdo.modules:
            #s += (s.noIndent() + ', "' + m["name"] + '":self.BEH')
        #s += (s.noIndent() + '}\n')

        #s += '# Set fdump to True in order to generate test vector files for the local interfaces\n'
        #s += 'self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}\n\n'

        #s += '# TO DO: Provide stimuli and reference files here\n'

        #for i in mfdo.interfaces:
            #if i["direction"]=='IN':
                #s += 'self.stim_' + i["name"] + '.append({"file" : self.test_path + "/vectors/stim_' + i["name"] + '.tvr"})\n'
            #elif i["direction"]=='OUT':
                #s += 'self.res_' + i["name"] + '.append({"file" : self.test_path + "/vectors/res_' + i["name"] + '.tvr"})\n'
                #s += 'self.ref_' + i["name"] + '.append({"file" : self.test_path + "/vectors/ref_' + i["name"] + '.tvr"})\n'
        #s.newLine()

        #s + 'self.run_it(checkfiles=True)\n\n\n'

    s += s.dedent() + '# ----------------------------------------------------------------------------\n'

    s.write(filename, overwrite = mfdo.overwrite)
