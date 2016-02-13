import pihdf
from pihdf import info, warn, err

import os
import os.path


class CommandChecker():
    '''|
    | TODO
    |________'''    
    def __init__(self, cl_arguments):

        self.arguments = cl_arguments

        self.arguments["test_recursive"]     = False
        self.arguments["test_with_coverage"] = False

        if self.arguments["MPATH"]:
            self.module_path            = True
            self.module_path_exist      = os.path.exists(self.arguments["MPATH"])

            self.arguments["file_name"] = os.path.basename(os.path.normpath(self.arguments["MPATH"])) + '.json'
            self.arguments.update({"mpath_exist": self.module_path_exist})
        else:
            self.module_path            = False
            self.module_path_exist      = False

            self.arguments["MPATH"]     = ""
            self.arguments["file_name"] = ""
            self.arguments.update({"mpath_exist": False})
        
        # Register command checkers
        self.check =  {
            'new'     : self.new,
            'add'     : self.add,
            'remove'  : self.remove,
            'update'  : self.update,
            'test'    : self.test,
            'convert' : self.convert,
            'clean'   : self.check_MPATH_exist,
            'delete'  : self.check_MPATH_exist,
            'webdoc'  : self.no_check,
            'version' : self.no_check
        }

        self.validate_command_syntax()
        self.check[ self.arguments["<command>"] ]()


    def check_MPATH_exist(self):
        if not self.module_path_exist:
            err("Module path does not exist")
            exit(0)


    def validate_command_syntax(self):
        if self.arguments["<command>"] not in self.check:
            err("Unknown command: " + self.arguments["<command>"])
            # An additional check
            self.check_MPATH_exist()
            exit(0)

        
    def new(self):
        if not self.module_path:
            err("Missing module path")
            info("Usage: module MPATH new")
            exit(0)


    def update(self):
        self.check_MPATH_exist()

        if self.arguments["<args>"] != [] and "recursive" not in self.arguments["<args>"]: # TODO: recursive or all?
            err("Wrong command option: " + str(self.arguments["<args>"]))
            info("Usage: module MPATH update [recursive]")
            exit(0)
            

    def add(self):
        self.check_MPATH_exist()
        if self.arguments["<args>"] == []:
            err("Missing Interface type")
            exit(0)

        if len(self.arguments["<args>"]) != 1:
            err("More arguments given.")
            self.usage_add()

        if self.arguments["-n"] == "None":
            err("Missing name.")
            self.usage_add()

        interface_type = self.arguments["<args>"][0]

        if interface_type == 'HSD':
            self.check_arguments(self.arguments["-d"], self.arguments["-w"])

        elif interface_type == 'Bus':
            self.check_arguments(self.arguments["-i"])

        elif interface_type == 'Parameter':
            self.check_arguments(self.arguments["-v"])

        elif interface_type == 'STAvln':
            self.check_arguments(self.arguments["-d"], self.arguments["-w"])

        else:
            err("Unknown type: " + interface_type)
            exit(0)

    
    def remove(self):
        self.check_MPATH_exist()
        
        if len(self.arguments["<args>"]) != 1:
            err("Wrong command format")
            info("Usage: module MPATH remove NAME")
            exit(0)


    def test(self):
        self.check_MPATH_exist()

        if "recursive" in self.arguments["<args>"]:
            self.arguments["test_recursive"] = True

        if "with-coverage" in self.arguments["<args>"]:
            self.arguments["test_with_coverage"] = True


    def convert(self):
        self.check_MPATH_exist()

        if len(self.arguments["<args>"]) > 1  or  \
               self.arguments["<args>"] != [] and \
                    (("verilog" not in self.arguments["<args>"]) and ("vhdl" not in self.arguments["<args>"])):
                   
            err("Wrong command option: " + str(self.arguments["<args>"]))
            info("Usage: module MPATH convert [verilog | vhdl]")
            exit(0)

        
    def no_check(self):
        pass


    # =======================================================================
    def check_arguments(self, *arg ):
        if 'None' in arg:
            self.usage_add()
            

    def usage_add(self):
        err("Wrong command format")
        info("Usage: module MPATH add <interface_type> -n <name> -d <direction> -w <width/fields> [-p <push>]")
        info("Usage: module MPATH add Bus              -n <name> -i <bus_type>")
        info("       module MPATH add Parameter        -n <name> -v <value>...")
        exit(0)
