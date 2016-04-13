import myhdl
from myhdl import *

import inspect
import re

import os, sys, imp
import fileinput
from time import gmtime, strftime
import shutil

import simplejson
import collections

import __builtin__

from ..interfaces import *
from ..           import mylog

from str_builder import StrBuilder

from top_class import print_module_class_file
from custom_interfaces import print_custom_interfaces_file, copy_custom_interfaces
from btest_class import print_btest_file
from utest_class import print_utest_file

from beh import print_beh_file, update_beh_file
from rtl import print_rtl_file

from verilog import print_wrap_file, print_verilog_file

from comp_list import print_compile_list_file

from dotty import print_dotty_file
from json import print_json_file


class MFDesign(object):
    '''|
    | Base class to generate pihdf design files and directory structure
    |________'''
    def __init__(self):

        self.module_name = ''

        self.Reset = None
        self.Clock = None

        self.interfaces = []
        self.local_interfaces = []
        self.custom_interfaces = []

        self.parameters = []
        self.local_parameters = []
        
        self.modules = []        
        self.verilog = {}
        
        # Files generated in a directory tree. The root is where the .json file is located
        self.c_path = ''
        self.src_path  = 'src'
        self.out_path  = 'out'
        self.test_path = 'test'
        
        full_path = os.path.realpath(__file__)
        dir_name = os.path.dirname(full_path)
        base_path, tail = os.path.split(dir_name)
            
        self.overwrite = False


    # -----------------------------------------------------------------------------
    def isKnown(self, interface_name):
        '''|
        | Checks whether a particular interface is 'known' and can be treated properly
        | A known interface is one which is imported by 'interfaces.py' file
        |________'''
        if interface_name in sys._getframe(1).f_locals  or \
           interface_name in sys._getframe(1).f_globals or \
           interface_name in vars(__builtin__):        
            return True
        else:
            mylog.warn("Interface type'" + interface_name + "' is unknown. The generated code may be incorrect!")
            return False


    def printInterfaces(self):
        '''|
        | Print the interfaces to string
        |________'''
        ss = ''
        if self.Reset != None:
            ss += self.Reset["name"] + ', '
            
        if self.Clock != None:
            ss += self.Clock["name"] + ', '  
                 
        for i in self.interfaces:
            ss += i["name"] + ', '
 
        for p in self.parameters:
            ss += p["name"] + ', '    

        return ss[:-2] if len(ss) > 1 else ss 


    def printMainInterfaces(self, s, fdump=False):
        FDUMP = 'FDUMP' if fdump else ''
        intfs_names = ''
        if self.interfaces:
            for i in self.interfaces:
                intfs_names += i["name"] + ', '
            s += intfs_names
            s = s-2 + (s.noIndent() + ' = self.get_interfaces(' + FDUMP + ')\n')


    def printBusInterfaces(self, s, j, bname):
        '''|
        | Print the Bus interfaces to string
        |________'''
        intfs_names = ''
        for k in j:
            intfs_names += k.inst_name + ', '
        s += intfs_names
        s = s-2 + (s.noIndent() + ' = ' + bname + '.interfaces()\n')


    def getInterfaceObj(self, i):
        '''|
        | Return a list of objects of interfaces.
        |________'''
        if "data" in i: # in case of HSD interface
            i_dir = 0 if i["direction"] == "IN" else 1
            intfs = eval(i["type"])(data = eval(i["data"]), direction = i_dir, name = i["name"])
            return [ intfs ]
        elif "interfaces" in i: # in case of a Bus interface
            intfs_list = eval(i["type"])(bus_type = eval(i["interfaces"]), name = i["name"]).interface_list
            return intfs_list
        else: # in case of STAvln interface
            i_width = int(i["width"])
            i_dir = 0 if i["direction"] == "IN" else 1
            intfs = eval(i["type"])(data_width = i_width, direction = i_dir, name = i["name"])
            return [ intfs ]


    def printSignals(self, s):
        '''|
        | Print the signals of the interfaces to string
        |________'''
        s += ''
        
        if self.Reset != None:
            s += (s.noIndent() + self.Reset["name"] + ', ')

        if self.Clock != None:
            s += (s.noIndent() + self.Clock["name"] + ',\n')       
        
        for i in self.interfaces:
            j = self.getInterfaceObj(i)

            for k in j:
                for sigName in k.get_sig_names():
                    s += k.inst_name + '_' + sigName + ','
                    s.noIndent()
                s += '\n'

        for p in self.parameters:
            s += p["name"] + ', '
            s.noIndent()
            
        s = s-2 + (s.noIndent() + ')')    


    def extractText(self, filename, begin_str, end_str):
        '''|
        | Extract text between pragmas from file. Pragmas are given via the begin_str and end_str arguments
        | The pragmas are not included in the extracted text
        |________'''
        s = ""
        try:
            with open(filename) as f:
                enable = False
                for line in f:
                    if line.startswith(end_str):
                        enable = False

                    if enable:
                        s += line

                    if line.startswith(begin_str):
                        enable = True

        except Exception as e:
            # 'False positive' in command 'new'
            # mylog.err("in extractText():")
            # print "      ", e
            pass

        return s


    # -----------------------------------------------------------------------------
    def initialize(self, filename):
        '''|
        | Initialize a pihdf design object
        |________'''
        f = open(filename)
        try:
            json_struct = simplejson.load(f, object_pairs_hook=collections.OrderedDict)
        except Exception as e:
            mylog.err("in initialize(), cannot load .json file: " + filename)
            print "      ", e
            sys.exit(1)
        f.close()

        self.interfaces        = []
        self.parameter         = []
        self.local_interfaces  = []
        self.custom_interfaces = []
        self.local_parameter   = []
        self.modules           = []
        
        head, tail = os.path.split(filename)
        self.c_path = head
        
        if 'custom_interfaces' in json_struct:
            self.custom_interfaces = json_struct['custom_interfaces']
            self.load_custom_interfaces(self.custom_interfaces)

        jdesign  = json_struct['design']    if 'design'    in json_struct else None
        jimplmn  = json_struct['structure'] if 'structure' in json_struct else None
        jverilog = json_struct['verilog']   if 'verilog'   in json_struct else None

        # -----------------------------------------------------------------------------
        for tag in jdesign.keys():
            if tag=='name':
                self.module_name = jdesign[tag]     
                
            if tag=='interfaces':    
#                 print jdesign[tag]
                interface_tmp_list = [] 
                for item in jdesign[tag]:
                    # add supported interface types only
                    if self.isKnown(item["type"]):
                        # CHECK for interfaces with the same name
                        assert( item["name"] not in interface_tmp_list), "ERROR: the name '{:}' of interface type '{:}' has been previously used!".format(item["name"], item["type"])
                        interface_tmp_list.append(item["name"])
          
                        if item["type"]=='Reset':
                            self.Reset = item                                   
                        elif item["type"]=='Clock':
                            self.Clock = item                
                        else :
                            self.interfaces.append(item)
                            
            if tag=='parameters':
                self.parameters = jdesign[tag]
                
        # -----------------------------------------------------------------------------
        if jimplmn != None:
            for tag in jimplmn.keys():             
                if tag=='local_interfaces':
                    interface_tmp_list = []    
                    for item in jimplmn[tag]:
                        # add supported interface types only
                        if self.isKnown(item["type"]): 
                            # CHECK for interfaces with the same name
                            assert( item["name"] not in interface_tmp_list), "ERROR: the name '{:}' of local interface type '{:}' has been previously used!".format(item["name"], item["type"])
                            interface_tmp_list.append(item["name"])
                            self.local_interfaces.append(item)
                                
                if tag=='local_parameters':
                    self.local_parameters = jimplmn[tag]
                   
                if tag=='design_modules':
                    for item in jimplmn[tag]:
                        m_dict = {}                    
                        for n in item.keys():
                            if n=="name":
                                m_dict[n]=item[n]
                            if n=="type":
                                m_dict[n]=item[n]
                            if n=="connections":
                                m_dict[n] = item[n]
                                for x in item[n]:
                                    m_dict[x["local_name"]]=x["connect_to"]
#                                     m_dict.update({x["local_name"]:x["connect_to"]})  
                                
                            if n=="path":
                                m_dict[n]=item[n]
                          
                        self.modules.append(m_dict)            
        # -----------------------------------------------------------------------------
        if jverilog != None:
            m_dict = {} 
            for tag in jverilog.keys():
                if tag=='name':    
                    m_dict[tag]=jverilog[tag]
                if tag=="path":
                    m_dict[tag]=jverilog[tag]
                  
            self.verilog = m_dict    


    def init_submodules(self):
        '''|
        | Initialize a new pihdf design object for each sub-module found in the .json file
        |________'''         
        sub_modules = []
        m_dict = {}
        for m in self.modules:
            if not m["type"] in m_dict and m["path"]=='':
                m_dict[m["type"]]=1
                 
                module = MFDesign()

                module.module_name = m["type"]
                
                for c in m["connections"]:
                    if c["connect_to"] == self.Reset["name"]:
                        module.Reset = self.Reset.copy()
                        module.Reset.update({"name":c["local_name"]})
                    elif c["connect_to"] == self.Clock["name"]:
                        module.Clock = self.Clock.copy()
                        module.Clock.update({"name":c["local_name"]})
                    else:                
                        for i in self.interfaces: 
                            if c["connect_to"] == i["name"]:
                                interface = i.copy()
                                interface.update({"name":c["local_name"]})
                                module.interfaces.append(interface)
    
                        for i in self.local_interfaces: 
                            if c["connect_to"] == i["name"]:
                                interface = i.copy()
                                interface.update({"name":c["local_name"]})
                                interface.update({"direction":c["direction"]})
                                module.interfaces.append(interface)
    
                        for p in self.parameters: 
                            if c["connect_to"] == p["name"]:
                                parameter = p.copy()
                                parameter.update({"name":c["local_name"]})
                                module.parameters.append(parameter)
    
                        for p in self.local_parameters: 
                            if c["connect_to"] == p["name"]:
                                parameter = p.copy()
                                parameter.update({"name":c["local_name"]})
                                module.parameters.append(parameter)
        
                sub_modules.append(module)
            
        return sub_modules   


    def load_custom_interfaces(self, package_list):
        '''|
        | Make the custom interfaces specified in the .json file visible in pihdf
        |________'''
        for p in package_list:
            pfile = self.c_path + '/' + p['file']
	    custom_interfaces = imp.load_source(p['name'], pfile)

	    for iname in dir(custom_interfaces):
	        itype = getattr(custom_interfaces, iname)
	        if isinstance(itype, list):
	            sys._getframe(0).f_globals[iname] = itype
        

    def generate(self, module_name):
        '''|
        | Generate the module design directory tree and files
        |________'''
        # Create the project directory structure 
        os.makedirs(self.c_path + '/' + self.src_path) 
        os.makedirs(self.c_path + '/' + self.out_path)
        os.makedirs(self.c_path + '/' + self.test_path)
        os.makedirs(self.c_path + '/' + self.test_path + '/vectors')
          
        mylog.head("Generating design files: " + module_name)   
           
        # Generate empty _init_ files
        StrBuilder().write(self.c_path + '/__init__.py', overwrite=True)
        StrBuilder().write(self.c_path + '/' + self.src_path + '/__init__.py', overwrite=True)  
        StrBuilder().write(self.c_path + '/' + self.test_path + '/__init__.py', overwrite=True) 
        # git hack
        StrBuilder().write(self.c_path + '/' + self.out_path + '/.gitignore', overwrite=True)  
        StrBuilder().write(self.c_path + '/' + self.test_path + '/vectors/.gitignore', overwrite=True)

        copy_custom_interfaces(self)
        print_module_class_file(self)
        print_btest_file(self)
        print_utest_file(self)
        print_compile_list_file(self)
       
        if self.modules == []:
            print_beh_file(self)
                        
            if self.verilog != {}: 
                if self.verilog["path"]=='':
                    # Generate a verilog file containing only the interface signals.
                    # Implementation to be provided by the designer.
                    print_verilog_file(self)
                else:    
                    # A third-party verilog module to be integrated
                    filename = self.verilog["path"] + '/' + self.verilog["name"] + '.v'
                    print_wrap_file(self, filename)
                    shutil.copyfile(filename, self.c_path + '/src/' + self.verilog["name"] + '.v')
            else:
                print_rtl_file(self)
        else:
            print_beh_file(self)
            print_rtl_file(self)


    def update_files(self):
        '''|
        | Update the module design files according to changes in .json file
        |________'''
        mylog.head("Updating and generating design files: " + self.module_name)   
        
        self.overwrite = True
        
        copy_custom_interfaces(self)
        print_module_class_file(self)
        print_btest_file(self)
        print_compile_list_file(self)
       
        if self.modules == []:
            update_beh_file(self)
                        
            if self.verilog != {}: 
                if self.verilog["path"]=='':
                    # Generate a verilog file containing only the interface signals.
                    # Implementation to be provided by the designer.
                    print_verilog_file(self)
                else:    
                    # A third-party verilog module to be integrated
                    filename = self.verilog["path"] + '/' + self.verilog["name"] + '.v'
                    print_wrap_file(self, filename)
                    shutil.copyfile(filename, self.c_path + '/src/' + self.verilog["name"] + '.v')
            else:
                print_rtl_file(self)
        else:
            update_beh_file(self)
            print_rtl_file(self)

            
    def update(self, file_name):
        self.initialize( file_name )
        self.update_files()

        if self.modules != []:
            sub_modules = self.init_submodules()

            print_dotty_file(self)

            if sub_modules != []: # is this check needed?
                sub_path = self.c_path + "/src/modules/"
                for m in sub_modules:
                    m.c_path = sub_path + m.module_name
                    m.overwrite = True
                    print_json_file(m)
                    m.update(m.c_path + '/' + m.module_name + '.json')
