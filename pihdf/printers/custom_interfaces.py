from str_builder import StrBuilder
import os

from .. import mylog

import sys, imp

def print_custom_interfaces_file(mfdo):
    '''|
    | Create 'interfaces.py' file containing custom fields interfaces defined in the .json file.
    | Comand 'update' modifies this file as well.
    |________'''
    if mfdo.custom_interfaces == []: return

    s = StrBuilder()
    filename = mfdo.c_path + "/interfaces.py"

    ss = ''
    indent = 0

    for interface in mfdo.custom_interfaces:
        for tag in interface.keys():
            if tag == 'name':                    
                sss = interface[tag] + ' = ['
                indent = len(sss) * ' '
                ss += sss

            if tag == 'fields': 
                for fields in interface[tag]:
                    ss += '("' + fields["name"] + '", ' + fields["type"] + '),\n' + indent

        ss = ss[:-len(indent)-2] + ']\n' # removes the last comma
        ss += '#-----------------------------------------------------------\n\n'

    s += "from myhdl import *\n\n" 
    s += ss

    s.write(filename, overwrite=True)

    # make the interface visible in pihdf
    custom_interfaces = imp.load_source('interfaces', filename)

    for iname in dir(custom_interfaces):
        itype = getattr(custom_interfaces, iname)
        if isinstance(itype, list):
            sys._getframe(1).f_globals[iname] = itype


