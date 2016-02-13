from str_builder import StrBuilder


def print_rtl_file(mfdo):
    '''|
    | Create <module_name>_rtl.py file
    | It is an empty (template) file used to specify (synthesizable) implementation at RTL
    | Interface signals are generated as well
    |________'''
    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + "_rtl.py"

    s += 'from myhdl import *\n'
    s += 'import pihdf\n'
    s += 'from pihdf import *\n'
    s += 'from myhdl_lib import *\n\n'

    if mfdo.modules != []:
        #s += 'import os\n\n'

        pp_dict = {}
        tt_dict = {}
        for p in mfdo.modules:
            if p["path"]=='':
                if not p["type"] in tt_dict:
                    tt_dict[p["type"]]=1
                    s += 'from modules.' + p["type"] + '.' + p["type"] + ' import ' + p["type"] + '\n'

            elif not p["path"] in pp_dict:
                if not p["type"] in tt_dict:
                    tt_dict[p["type"]] = 1
                    # TODO: Not clear how to deal with the import paths!!!
                    s += 'from ' + p["type"] + '.' +  p["type"] + ' import ' + p["type"] + '\n'
                    #spath = p["path"][3:].replace("/", ".")
                    #s += 'from ' + spath + ' import ' + p["type"] + '\n'
        s += s.noIndent() + '\n'

    s += '#--- Custom code begin ---#\n'
    s += s.noIndent() + mfdo.extractText(filename, "#--- Custom code begin ---#", "#--- Custom code end   ---#")
    s += "#--- Custom code end   ---#\n\n"

    s += 'def ' + mfdo.module_name + '_rtl('
    s += s.noIndent() + mfdo.printInterfaces()
    if mfdo.modules != []:
        s += s.noIndent() + ', IMPL, FDUMP):\n'
    else:
        s += s.noIndent() + '):\n'

    s += s.indent() + s.header_comment('Top-level MyHDL description. This is converted to RTL velilog...')
    s.newLine()
    s += '""" Interface signals """\n'
    for i in mfdo.interfaces:
        j = mfdo.getInterfaceObj(i)
        if len(j) > 1:
            mfdo.printBusInterfaces(s, j, i["name"])

        for k in j:
            stype  = '.get_src_signals() # produce data\n' if k.direction == 1 else '.get_snk_signals() # consume data\n'
            snames = ', '.join(k.get_sig_full_names())
            s += snames + " = " + k.inst_name + stype

    s += s.noIndent() + '\n'

    #-------------------------------------------------------------------------------------------
    # generate an empty (template) file used to specify RTL (synthesizable) implementation
    #-------------------------------------------------------------------------------------------
    if mfdo.modules == []:
        s += '#--- Custom code begin ---#\n'
        s += s.noIndent() + mfdo.extractText(filename, "    #--- Custom code begin ---#", "    #--- Custom code end   ---#")
        s += "#--- Custom code end   ---#\n\n"
        s += 'return all_instances(' + mfdo.Reset["name"] + ', ' + mfdo.Clock["name"] + ')\n'

    else:
        #---------------------------------------------------------------------------------------
        # generate the gen() body (connected components given in the .json file)
        #---------------------------------------------------------------------------------------

        # declaration of the interfaces
        s += '""" Local interfaces """\n'
        for i in mfdo.local_interfaces:
            s_tmp       =                  i["width"]     if("width"  in i)    else \
                          'data='        + i["data"]      if("data"   in i)    else ''
            s_buf_size  = ', buf_size='  + i["buf_size"]  if("buf_size"  in i) else ''
            s_push      = ', push='      + i["push"]      if("push"   in i)    else ''
            s_terminate = ', terminate=' + i["terminate"] if "terminate" in i  else ''
            s += i["name"] + ' = ' + i["type"] + '(' + s_tmp + s_buf_size + s_push + s_terminate + ', filedump=FDUMP)\n'
        s += s.noIndent() + '\n'

        # declaration of the local parameters
        if mfdo.local_parameters != []:
            s += '# Parameters\n'
            for p in mfdo.local_parameters:
                s += p["name"] + ' = ' + p["value"] + '\n'
            s.newLine()

        s += 'if isinstance(IMPL, dict):\n'
        s.indent()
        cc = 1
        for m in mfdo.modules:
            inst_name = m["name"] if "name" in m else 'inst_' + m["type"] + str(cc)
            s += inst_name + '_impl = IMPL["' + inst_name + '"] if "' + inst_name + '" in IMPL else IMPL["top"]\n'
            cc += 1
        s += s.dedent() + 'else:\n'
        s.indent()
        cc = 1
        for m in mfdo.modules:
            inst_name = m["name"] if "name" in m else 'inst_' + m["type"] + str(cc)
            s += inst_name + '_impl = IMPL\n'
            cc += 1
        s.dedent()
        s += s.noIndent() + '\n'

        # instance of the modules (and port map)
        s += '""" Components """\n'
        cc = 1

        for m in mfdo.modules:
            inst_name = m["name"] if "name" in m else 'inst_' + m["type"] + str(cc)
            s += inst_name + ' = ' + m["type"] + '(' + inst_name + '_impl).gen('
            cc += 1
            for key, value in m.iteritems():
                if key != "name" and key != "path" and key != "type" and key != "connections":
                    s.noIndent()
                    s += key + '=' + value + ', '

            s = s-2 + (s.noIndent() + ')\n') # remove the last comma
        s += s.noIndent() + '\n'

        s += '#--- Custom code begin ---#\n'
        s += s.noIndent() + mfdo.extractText(filename, "    #--- Custom code begin ---#", "    #--- Custom code end   ---#")
        s += "#--- Custom code end   ---#\n"

        s.newLine()
        s += 'return all_instances(' + mfdo.Reset["name"] + ', ' + mfdo.Clock["name"] + ')\n'

    s.write(filename, overwrite = mfdo.overwrite)
