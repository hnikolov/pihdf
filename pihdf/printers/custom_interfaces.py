from str_builder import StrBuilder
import os

from .. import mylog

import os, sys, imp

import shutil

def copy_custom_interfaces(mfdo):
    '''|
    | Copy the specified custom interfaces to module/imp/ directory.
    |________'''
    if mfdo.custom_interfaces == []: return

    m_path = mfdo.c_path + '/imp/'

    if os.path.exists( m_path ): # In case of command 'update'
        shutil.rmtree(m_path, ignore_errors=True)

    os.makedirs( m_path )
    StrBuilder().write(m_path + '__init__.py', overwrite=True)

    for p in mfdo.custom_interfaces:
        pfile = mfdo.c_path + '/' + p['file']
        shutil.copy(pfile, m_path + p['name'] + '.py')


def print_custom_interfaces_file(mfdo):
    '''|
    | TODO: OBSOLETE. Create 'interfaces.py' file containing custom fields interfaces defined in the .json file.
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


#    locals()['my_module'] = __import__(mfdo.c_path + '/interfaces.py')
