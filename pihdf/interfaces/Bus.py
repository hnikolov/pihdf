import traceback

from myhdl import *
from collections import OrderedDict
from RegFile import RegFile


class Bus(object):
    '''|
    | A generic Bus class. This class is a container containing interfaces used to specify a bus.
    | Interfaces can be any of the supported interfaces in pihdf.
    | A Bus is defined by a list of 'interfaces' in file 'fields_interfaces.py', part of pihdf.
    |________'''    
    def __init__(self, bus_type=None, name=None, reg_file=False, filedump=None, lo=-2):

        self.interface_list = bus_type()
        self.reg_file = reg_file
                    
        if name == None:
            # Extract the instance name
            (filename,line_number,function_name,text)=traceback.extract_stack()[lo]
            self.inst_name = text[text.find('.')+1:text.find('=')].strip()  # skip 'self.'
            if self.inst_name=='':
                self.inst_name = text[:text.find('=')].strip()
        else:
            self.inst_name = name

        self.class_name = self.__class__.__name__

        if self.reg_file:
            self.ctrl = RegFile()

        for i in self.interface_list:
            i.inst_name = self.inst_name + "_" + i.inst_name


    def interfaces(self):
        '''|
        | Return the list of interfaces. If the list contains only one interfaces, then returns the interface itself.
        |________'''
        if len(self.interface_list) == 1:
            return self.interface_list[0]
        return self.interface_list


    def get_all_signals(self):
        '''|
        | Return OrderedDict of all signals of all bus interface.
        |________'''
        return OrderedDict([(name, signal) for interface in self.interface_list for name, signal in interface.get_all_signals().iteritems()])


    def assign(self, *args):
        '''|
        | Assigns all all signals of all bus interface.
        |________'''
        a = args
        ls_assign = []

        for interface in self.interface_list:
            num_signals = len(interface.get_all_signals())
            signals = a[:num_signals]
            ls_assign.append(interface.assign(*signals))
            a = a[num_signals:]

        return ls_assign


    def create_reg_file(self, rst, clk, filename=""):
        if self.reg_file:
            return self.ctrl.create_reg_file(rst, clk, self.interface_list[0], self.interface_list[1], self.interface_list[2], filename)
        else:
            return []

