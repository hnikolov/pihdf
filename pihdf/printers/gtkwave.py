from str_builder import StrBuilder
from ..          import mylog


def print_gtkw_file(mfdo, cosim = False):
    '''|
    | GTKW file to visualize vcd traces from simulation
    |________'''
    str_cosim = ''
    dut = mfdo.module_name + "_top" + '.'
    if cosim:
        dut = "tb_" + mfdo.module_name + "_top" + ".dut."
        str_cosim = '_cosim'

    s = StrBuilder()
    stmp = str_cosim + ".gtkw" if cosim else ".gtkw"
    filename = mfdo.c_path + '/' + mfdo.test_path + '/' + mfdo.module_name + stmp

    try:
        with open(filename) as f: mylog.info("File '%s' found. It will NOT be updated!" % filename)

    except IOError as e:
        s += '[dumpfile] "' + mfdo.c_path + '/' + mfdo.module_name + '/out/'  + mfdo.module_name + '_top' + str_cosim + '.vcd"\n'
        s += '[savefile] "' + mfdo.c_path + '/' + mfdo.module_name + '/test/' + mfdo.module_name + '_top' + str_cosim + '.gtkw"\n'

        s += "[timestart] 0\n"
        s += "[pos] -1 -1\n"
        s += "[treeopen] tb_" + mfdo.module_name  + "_top" + ".\n"
        s += "[sst_expanded] 1\n"

        s += dut + mfdo.Reset["name"] + "\n"
        s += dut + mfdo.Clock["name"] + "\n"

        # print the interface signals
        for i in mfdo.interfaces:
            j = mfdo.getInterfaceObj(i)
            iname = i["name"] + '_' if len(j) > 1 else ''
            for k in j:
                xtra = 'rtl.' if not cosim else ''
                s += "-\n"

                cname = '_' + k.inst_name.upper() if len(j) > 1 else ''
                if k.direction == 1: s += "-" + i["name"].upper() + cname + " (OUT)\n"
                else:           s += "-" + i["name"].upper() + cname + " (IN)\n"

                for sigName, sigLen in zip(k.get_sig_names(), k.get_sig_lens()):
                    ss = "[" + str(sigLen-1) + ":0]" if (sigLen > 1) else ''
                    s += dut + xtra + iname + k.inst_name + '_' + sigName + ss + "\n"

        s.write(filename, overwrite=True)
