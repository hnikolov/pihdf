import myhdl
from str_builder import StrBuilder


def print_module_class_file(mfdo):
    '''|
    | Create <module_name>.py file
    |________'''
    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.module_name + ".py"
    #--------------------------------------------------------------------------------------------
    # imports
    #--------------------------------------------------------------------------------------------
    s += 'from myhdl import *\n'
    s += 'from pihdf import Convertible\n'
    s += 'from pihdf.interfaces import *\n\n'

    if mfdo.modules != []:
        # TODO: Needs rethinking in case of structural designs 
        s += 'import sys\n'
        s += 'import os\n'
        s += 'module_path = os.path.dirname(__file__)\n\n'
        # Make third-party-modules 'visible'
        p_dict = {}
        t_dict = {}
        bflg = 0
        for p in mfdo.modules:
            if p["path"]=='':
                bflg += 1
            elif not p["path"] in p_dict:
                # TODO: Not clear how to deal with the import paths!!!
                s += 'lib_path = os.path.abspath(module_path + "/../' +  p["path"] + '")\n'
                s += 'sys.path.append(lib_path)\n'
                p_dict[p["path"]] = 1
        s.newLine()
        if bflg > 1:
            # Make the modules in directory 'modules' visible for each other
            s += "import site\n"
            s += "site.addsitedir(module_path + '/src/modules')\n\n"

    for p in mfdo.custom_interfaces:
        s += 'from imp.' + p['name'] + ' import *\n\n'

    s += 'from ' + 'src.' + mfdo.module_name + '_beh import *\n'
    if mfdo.verilog != {}:
            s += 'from ' + 'src.' + mfdo.module_name + '_wrp import *\n'
    else:
            s += 'from ' + 'src.' + mfdo.module_name + '_rtl import *\n'
    s.newLine()

    s += 'class ' + mfdo.module_name + '(Convertible):\n'
    s += s.indent() + s.header_comment('The design class')

    s += 'def __init__(self, IMPL={}):\n\n'
    s.indent()

    if mfdo.modules != []:
        s += 'self.structural = True\n'
        s += 'self.models = IMPL\n'
    else:
        s += 'self.structural = False\n'
    s.newLine()

    s += 'if isinstance(IMPL, dict):\n'
    s += s.indent() + 'self.IMPL = IMPL["top"] if "top" in IMPL else IMPL\n'
    s += s.dedent() + 'else:\n'
    s += s.indent() + 'self.IMPL = IMPL\n\n'

    s += s.dedent() + '# call base class constructor\n'
    s += 'Convertible.__init__(self)\n\n'

    # TODO: To be extended for any number of reset signals
    s += 'self.resets = lambda : [\n'
    s += s.indent() + 'Reset(name="' + mfdo.Reset["name"] + '", active=' + mfdo.Reset["active"] + ', val=' + mfdo.Reset["active"] + ', async=True)\n'
    s += s.dedent() + ']\n'

    s.newLine()

    # TODO: To be extended for any number of clock signals
    s += 'self.clocks = lambda : [\n'
    s += s.indent() + 'Clock(name="' + mfdo.Clock["name"] + '")\n'
    s += s.dedent() + ']\n'

    s.newLine()

    s += "self.interfaces = lambda fdump : [\n"
    s.indent()

    for i in mfdo.interfaces:
        s_width     = 'data_width='      + i["width"]        + ', ' if "width"      in i else ''
        s_direction = 'direction=self.'  + i["direction"]    + ', ' if "direction"  in i else ''
        s_intfs     = 'bus_type='        + i["interfaces"]   + ', ' if "interfaces" in i else ''
        s_name      = 'name="'           + i["name"] + '"'   + ', ' if "name"       in i else ''
        s_data      = 'data='            + i["data"]         + ', ' if "data"       in i else ''
        s_push      = 'push='            + i["push"]         + ', ' if "push"       in i else ''
        s_regfile   = 'reg_file='        + i["reg_file"]     + ', ' if "reg_file"   in i else ''
        s += i["type"] + '(' + s_width + s_direction + s_intfs + s_name + s_data + s_push + s_regfile
        s += s.noIndent() + 'filedump=fdump),\n'

    s = s-2 + (s.noIndent() + '\n')
    s += s.dedent() + ']\n'
    
    s.newLine()
    
    if mfdo.parameters != []:
        s += '# no lambda here\n'
        s += 'self.parameters = [\n'
        s.indent()

        for p in mfdo.parameters:
            s += 'Parameter("' + p["name"] + '", value=' + p["value"] + '),\n'
        
        s = s-2 + '\n' # remove the last comma
        s += s.dedent() + ']\n'
    else:
        s += 'self.parameters = []\n'

    s.newLine()

    s += '# register implementations used in Convertible.gen()\n'
    s += 'self.funcdict = {\n'
    s.indent()

    s_beh = mfdo.module_name + "_beh"
    s_rtl = mfdo.module_name + "_rtl" if mfdo.verilog == {} else "None"
    s_vrg = mfdo.module_name + "_wrp" if mfdo.verilog != {} else "None"

    s += "'beh': " + s_beh + ",\n"
    s += "'rtl': " + s_rtl + ",\n"
    s += "'vrg': " + s_vrg + "\n"
    s += s.dedent() + '}\n'

    s.dedent()
    s.newLine(2)

    generateTop(mfdo, s)
    s.newLine(2)

    s += s.dedent(3) + 'if __name__ == "__main__":\n\n'

    s += s.indent() + 'import myhdl\n'
    s += 'import pihdf\n\n'

    s += 'pihdf.info("Using MyHDL version %s" % myhdl.__version__)\n'
    s += 'pihdf.info("Using MyFramework version %s" % pihdf.__version__)\n\n'

    s += 'dn = ' + mfdo.module_name + '(IMPL=1)\n'

    sparams = ''
    if mfdo.parameters != []:
        sparams += ', params={'
        for p in mfdo.parameters:
            sparams += '"' + p["name"] + '":' + p["value"] + ', '
        sparams = sparams[:-2] + '}'# remove the last comma
        
    s += 'dn.convert(hdl="verilog"' + sparams + ')\n'
    s += 'dn.convert(hdl="vhdl"'    + sparams + ')\n'
    s += 'dn.clean()\n'

    s.write(filename, overwrite = mfdo.overwrite)


def generateTop(mfdo, s):
    '''|
    | Generate function top()
    |________'''
    s += "def top(self,\n"
    s.indent(2)
    mfdo.printSignals(s)
    s += s.noIndent() + ':\n'
    
    s += s.dedent() + s.header_comment('Provides flat interface to the top-level implementation. This function is given to MyHDL.toVerilog() and MyHDL.toVHDL()')
    s += "x = locals()\n"
    s += "del x['self']\n"
    s += "return self.flat2struct(**x)\n"
