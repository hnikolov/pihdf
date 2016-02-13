from str_builder import StrBuilder

def print_beh_file(mfdo):
    '''|
    | Create <module_name>_beh.py file. It is an empty (template) file used to model behavior
    |________'''
    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + "_beh.py"

    if mfdo.interfaces or mfdo.parameters:
        s += 'def ' + mfdo.module_name + '_beh('
        for i in mfdo.interfaces:
            s += s.noIndent() + i["name"] + ', '
        for p in mfdo.parameters:
            s += s.noIndent() + p["name"] + ', '
        s = s-2 + (s.noIndent() + '):\n')
    else: # we start without a .json file, so the interface and parameter lists are empty
        s += 'def ' + mfdo.module_name + '_beh():\n'

    s += s.indent() + s.header_comment('Specify the behavior, describe data processing; there is no notion of clock. ' + \
                        'Access the in/out interfaces via get() and append() methods. ' + \
                        'The "' + mfdo.module_name + '_beh" function does not return values.')

    s.newLine()        
    s += 'print "Warning: Behavior model not implemented yet!"\n\n'
    s.write(filename)


def update_beh_file(mfdo):
    '''|
    | Update <module_name>_beh.py file containing custom code used to model behavior
    |________'''
    s = StrBuilder()
    filename = mfdo.c_path + '/' + mfdo.src_path + '/' + mfdo.module_name + "_beh.py"

    with open(filename) as f_old:
        for line in f_old:
            if line.startswith("def " + mfdo.module_name):

                if mfdo.interfaces or mfdo.parameters:
                    s += 'def ' + mfdo.module_name + '_beh('
                    for i in mfdo.interfaces:
                        s += s.noIndent() + i["name"] + ', '
                    for p in mfdo.parameters:
                        s += s.noIndent() + p["name"] + ', '
                    s = s-2 + (s.noIndent() + '):\n')
                else: # the interface and parameter lists are empty
                    s += 'def ' + mfdo.module_name + '_beh():\n'

            else:
                s += line

    s.write(filename, overwrite = mfdo.overwrite)
