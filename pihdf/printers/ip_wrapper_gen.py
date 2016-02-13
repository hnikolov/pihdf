from myhdl import *
from str_builder import StrBuilder

import os
import sys


class GenWrapperFile(object):
    '''|
    | This class is used to generate a python wrapper of a verilog design
    |________'''

    def __init__(self):

        self.module_name = ''
        self.interface = []  # keeps the order of the declarations
        self.parameters = []
        self.inputs = []
        self.outputs = []


    def generateWrapperFile(self):
        '''|
        | Generate <module_name_wrapper>.py file
        |________''' 
        print "\nGenerating .py wrapper file."   
  
        s = StrBuilder()
        
        self.genWrapperInterface(s)
        
        s += '# Need this in order to work...\n'
        # We assume that the clock is 'clk'!!!!!
        s += '@always(clk.posedge)\n'
        s += 'def pass_thru():\n'
        s += s.indent() + 'pass\n\n'       
        s.dedent()
 
        self.genTheWrapper(s)
        self.genConvertFunc(s)
        
        filename = self.module_name + '_wrp.py'
        s.write(filename)


    def genWrapperInterface(self, s):
        '''|
        | Generate the interfaces of the wrapper file
        |________'''
        s += 'from myhdl import *\n\n'          
        s += 'def ' + self.module_name + '_wrapper(\n'
 
        s.indent(5)
        for i in self.interface: # to preserve the order
             if i['type'] != 'parameter':
                 s += i['name'] + ',\n'
 
        s+= 'INST_NAME = "' + self.module_name.upper() + '",\n'
        
        for p in self.parameters:
             s += p['name'] + ' = ' + p['value'] + ',\n'           
        s -= 2 
        s += s.noIndent() + '):\n\n'
        
        s.dedent(3)
       

    def genTheWrapper(self, s, py_name=None):
        '''|
        | Generate the wrapper
        |________'''    
        s += '#---------------------------------------------#\n'
        s += '# Define the interface to the verilog ip core #\n'
        s += '#---------------------------------------------#\n'
        str_name = self.module_name if py_name == None else py_name
        s += str_name + '_wrp.verilog_code = \\' + '\n'
        if self.parameters != []:
            s += '"""' + self.module_name + '#(\\n""" + \\' +  '\n'
            
            for p in self.parameters:
                s += '"""    .' + p["name"] + '($' + p["name"] + '),\\n""" + \\' + '\n'
            s = s-11 + (s.noIndent() + '\\n""" + \\' + '\n')
            
            s += '"""    ) $INST_NAME (\\n""" + \\' + '\n'
        else:
            s += '"""' + self.module_name + ' $INST_NAME (\\n""" + \\' + '\n'
                
        for i in self.interface:
            if i["type"] != "parameter":
                s += '"""    .' + i["name"] + '($' + i["name"] + '),\\n""" + \\' + '\n'
        s = s-11 + (s.noIndent() + '\\n""" + \\' + '\n')
        s += '""");"""\n\n'
         
        s += '#-------------------------------------------------------#\n'
        s += '# output, needed when converting the wrapper to verilog #\n'
        s += '#-------------------------------------------------------#\n'                
        for o in self.outputs:      
            s += o["name"] + '.driven = "wire"\n'
        s += '\n'
        s += 'return pass_thru\n\n\n'
       

    def genConvertFunc(self, s):
        '''|
        | Generate function convert()
        |________'''
        s += s.noIndent() + 'def convert():\n\n'
        for i in self.parameters:
            s += i['name'] + ' = ' + i['value'] + '\n'           
        s += '\n'
        # Declare signals
        for i in self.interface:
            if i['type'] != 'parameter':
                x = i["size"]
                stype = 'bool(0)'
                if x.startswith('['): 
                    stype = 'intbv(0)'
                    x = x.replace(":0", "+1:")
                s += i['name'] + '= Signal(' + stype + x + ')\n'
        s += '\n'                
        s += 'toVerilog(' + self.module_name + '_wrapper,\n' 
        s.indent(2)
        for i in self.interface: 
            if i['type'] != 'parameter':
                s += i['name'] + ' = ' + i['name'] + ',\n'
 
        for p in self.parameters:
            s += p['name'] + ' = ' + p['name'] + ',\n'           
        s = s-2 + (s.noIndent() + ' )\n\n\n') 
        
        s.dedent(4)        
        s += 'if __name__ == "__main__":\n'
        s += s.indent() + 'convert()\n'      
                

    def initialize(self, filename):
        '''|
        | Initialize the GenWrapperFile object
        |________'''
        with open(filename) as f:
                     
            for line_number, line in enumerate(f):
                w_list = line.split()
                if w_list != []:
    
                    if w_list[0]=='module':
                        self.module_name = w_list[1]
    
                    elif w_list[0] == 'parameter':
                        name = w_list[1].replace(',','')
                        value = w_list[3].replace(',','')
                        self.parameters.append( {'name':name, 'value':value})
                        self.interface.append(  {'name':name, 'value':value, 'type':w_list[0]})
    
                    elif w_list[0] == 'input' or w_list[0] == 'output':
                        name = w_list[3] if w_list[2].startswith('[') else w_list[2] 
                        size = w_list[2] if  w_list[2].startswith('[') else ''
                        if w_list[0] == 'input':
                            self.inputs.append( {'name':name.replace(',',''), 'size':size})
                        elif w_list[0] == 'output':
                            self.outputs.append({'name':name.replace(',',''), 'size':size})
                        self.interface.append(  {'name':name.replace(',',''), 'size':size, 'type':w_list[0]})
    
                    elif w_list[0] == ');': 
                        break


def main( args ):
    
    gwf = GenWrapperFile()      
    gwf.initialize(args.file_name)  
    gwf.generateWrapperFile()

          
import argparse
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a myhdl wrapper file.')   
    parser.add_argument('-f', '--file', dest='file_name', default="",
                       help='top-level verilog (.v) file')
    args = parser.parse_args()
    
    main( args )          