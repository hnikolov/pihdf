from str_builder import StrBuilder
import os

from .. import mylog

def print_compile_list_file(mfdo):
    '''|
    | Create 'compile_list.txt' file containing a default list of verilog files used in case of co-simulation
    | All verilog files, which are part of the MyHDL design but are not auto-generated must be specified in this 'compile_list.txt' file
    |________'''
    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.src_path + '/compile_list.txt'
    filepath = os.getcwd() + '/' + mfdo.c_path + '/' + mfdo.src_path

    s += mfdo.module_name + '_top.v\n'

    if mfdo.verilog != {}:
        ls = extractFileNames(filename, mfdo)

        if ls == []:
            if mfdo.verilog["path"] == '':
                s += filepath + '/' + mfdo.module_name + '.v\n'
            else:
                s += filepath + '/' + mfdo.verilog["name"] + '.v\n'
        else:
            for l in ls:
                s += filepath + l + '\n'

    s += 'tb_' + mfdo.module_name + '_top.v\n'
    s.write(filename, overwrite = mfdo.overwrite)


def extractFileNames(filename, mfdo):
    '''|
    | Extract the names of the 'additional' custom verilog files used to implement the verilog design
    | Assumes that the files are located inside the module's source directory
    |________'''
    ls = []
    try:
        with open(filename) as f:
            for line in f:
                if mfdo.src_path in line:
                    ls.append( line.partition(mfdo.src_path)[2].strip() )

    except Exception as e:
        mylog.err("in extractFileNames():")
        print "      ", e

    return ls
