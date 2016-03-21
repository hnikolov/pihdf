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
            
    s += '#--- Add files begin ---#\n'
    # TODO: We should somehow update the relative path to the verilog files. Currently, we do nothing."
    s += s.noIndent() + mfdo.extractText(filename, "#--- Add files begin ---#", "#--- Add files end   ---#")
    s += "#--- Add files end   ---#\n"
            
    s += 'tb_' + mfdo.module_name + '_top.v\n'
    s.write(filename, overwrite = mfdo.overwrite)
