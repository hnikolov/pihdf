from str_builder import StrBuilder
from ip_wrapper_gen import GenWrapperFile

def print_wrap_file(mfdo, v_fname=None):
    '''|
    | Create <module_name>_wrp.py file
    | This file is used to integrate third-party verilog module in a MyHDL design
    | The verilog module must have the same interface signals as the generated in this file signals
    | All verilog implementation files must be specified in file 'compile_list.txt' file in order to be included for co-simulation
    |________'''
    if v_fname != None:
        verilog_file = v_fname
    else:
        verilog_file = mfdo.verilog["path"] + '/' + mfdo.verilog["name"] + '.v'

    gwf = GenWrapperFile()
    gwf.initialize(verilog_file)

    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + "_wrp.py"

    s += 'from myhdl import *\n\n'
    s += 'def ' + mfdo.module_name + '_wrp('
    s += s.noIndent() + mfdo.printInterfaces()
    s += s.noIndent() + ', INST_NAME):\n\n'

    s += s.indent() + '""" Interface signals """\n'

    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        if len(j) > 1:
            mfdo.printBusInterfaces(s, j, i["name"])

        iname = i["name"] + '_' if len(j) > 1 else ''
        for k in j:
            for sigName in k.get_sig_names():
                s += iname + k.inst_name + "_" + sigName + ","
                s.noIndent()

            stmp = ".get_src_signals() # produce data\n" if k.direction == 1 else ".get_snk_signals() # consume data\n" # 1=Out
            s = s-1 + (s.noIndent() + " = " + iname + k.inst_name + stmp)
    s.newLine()

    s += '# Need this in order to work...\n'
    s += '@always(' + mfdo.Clock["name"] + '.posedge, ' + mfdo.Reset["name"] + ')\n'
    s += 'def pass_thru():\n'
    s += s.indent() + 'pass\n\n'
    s.dedent()

    gwf.genTheWrapper(s)

    s.write(filename, overwrite = mfdo.overwrite)

            
def print_verilog_file(mfdo):
    '''|
    | Create <module_name>.v file
    | It is an empty (template) verilog file containing the interface signals, which must be used to integrate a
    | verilog module in a MyHDL design. The integration is done by using the auto-generated verilog wrapper file
    | The verilog module implementation has to be provided in this, and possibly other, files by the designers
    | Additional verilog files must be specified in file 'compile_list.txt' in order to be included for co-simulation
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + '.v'

    s += 'module ' + mfdo.module_name
    if mfdo.parameters != []:
        s.newLine()
        s += s.indent(2) + '#(\n'
        for p in mfdo.parameters:
            s += 'parameter ' + p["name"] + ' = ' + p["value"] + ',\n'
        s = s-2 + '\n'
        s += ')(\n'
    else:
        s += ' (\n'
        s.indent(2)

    if mfdo.Reset != None:
        s += 'input  wire \t\t' + mfdo.Reset["name"] + ',\n'
    else:
        print "Warning: RESET signal not specified!"

    if mfdo.Clock != None:
        s += 'input  wire \t\t' + mfdo.Clock["name"] + ',\n'
    else:
        print "Warning: CLOCK signal not specified!"

    for i in mfdo.interfaces:
        s.newLine()
        j = mfdo.getInterfaceObj(i)
        if len(j) > 1:
            s += '// ' + i["name"] + ' (Bus interface)\n'
            
        # print the interface signals
        iname = i["name"] + '_' if len(j) > 1 else ''
        for k in j:
            itype   = ' (consume data)\n' if k.direction == 0 else ' (produce data)\n'
            s += '// ' + iname + k.inst_name + itype
            
            for sigName, sigLen in zip(k.get_sig_names(), k.get_sig_lens()):
                str_dir = 'input  ' if k.direction == 0 else 'output '
                if sigName=='ready':
                        str_dir = 'input  ' if str_dir=='output ' else 'output '

                sigLenStr = '    \t' if sigLen==1 else '[' + str(sigLen-1) + ':0]\t'
                s += str_dir + 'wire ' + sigLenStr + iname + k.inst_name + '_' + sigName + ',\n'
        
    s = s-2 + '\n'
    s += ');\n\n'
    s.dedent(2)

    s += '/* Custom code begin */\n'
    s += s.noIndent() + mfdo.extractText(filename, "/* Custom code begin */", "/* Custom code end */")
    s += "/* Custom code end */\n\n"
    
    s += 'endmodule\n'
    
    s.write(filename, overwrite = mfdo.overwrite)

    print_wrap_file(mfdo, filename)

