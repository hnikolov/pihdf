from str_builder import StrBuilder
import os

def print_compile_list_file(mfdo):
    '''|
    | Create 'compile_list.txt' file containing a default list of verilog files used in case of co-simulation
    | All verilog files, which are part of the MyHDL design but are not auto-generated must be specified in this 'compile_list.txt' file
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.src_path + '/compile_list.txt'

    s += mfdo.module_name + '_top.v\n'
    if mfdo.verilog != {}:
        if mfdo.verilog["path"]=='':
            s += os.getcwd() + '/' + mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + '.v\n'
        else:
            s += os.getcwd() + '/' + mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.verilog["name"] + '.v\n'
    s += 'tb_' + mfdo.module_name + '_top.v\n'
    s.write(filename, overwrite = mfdo.overwrite)
