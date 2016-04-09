import myhdl
import myhdl_lib
import pihdf
from pihdf import MFDesign, StrBuilder, info, warn, err
from pihdf.printers.dotty import print_dotty_file
from pihdf.printers.json import print_json_file

import os
import os.path

import shutil

import webbrowser


class CommandHandler():
    '''|
    | TODO
    |________'''    
    def __init__(self, cl_arguments):

        self.module_path   = cl_arguments["MPATH"]
        self.file_name     = cl_arguments["file_name"]
        self.command       = cl_arguments["<command>"]
        self.arguments     = cl_arguments["<args>"]
        self.opt_Name      = cl_arguments["-n"]
        self.opt_Direction = cl_arguments["-d"]
        self.opt_Push      = cl_arguments["-p"]
        self.opt_Data      = cl_arguments["-w"]
        self.opt_BusType   = cl_arguments["-i"]
        self.opt_ParValue  = cl_arguments["-v"]

        self.full_name = self.module_path + '/' + self.file_name
        
        self.status = 0 # Used to return the status of executing the tests

        # Register command handlers
        self.handle = {
            'new'     : self.on_new,
            'add'     : self.on_add,
            'remove'  : self.on_remove,
            'update'  : self.on_update,
            'test'    : self.on_test,
            'convert' : self.on_convert,
            'clean'   : self.on_clean,
            'delete'  : self.on_delete,
            'webdoc'  : self.on_webdoc,
            'version' : self.on_version
        }

        self.handle[ self.command ]()


    def on_new(self):
        '''|
        | Command new creates a new module project from a .json file located in MPATH.
        | The json file must have the same name as the directory in which it is located.
        | If directory and/or .json file do not exist, this function creates the directory
        | and a default .json file (containing only Reset and Clock interfaces).
        |________'''
        self.check_path_and_create_json( self.full_name )

        gdf = MFDesign()
        gdf.initialize( self.full_name )
        gdf.generate(gdf.module_name + ' (top)')

        if gdf.modules != []:
            sub_modules = gdf.init_submodules()

            print_dotty_file(gdf)

            if sub_modules != []:
                sub_path = gdf.c_path + "/src/modules/"
                os.mkdir(sub_path)
                StrBuilder().write(sub_path + '__init__.py', overwrite=True)
                for m in sub_modules:
                    m.c_path = sub_path + m.module_name
                    m.generate(m.module_name + ' (sub-module)')
                    print_json_file(m)        


    def on_update(self):
        '''|
        | Command update re-generates the files, which are created with command new.
        | This command is useful when, e.g., HW module's interfaces or structure changes.
        | First, the corresponding .json file is modified capturing the changes.
        |________'''
        recursive = "recursive" in self.arguments
        
        if recursive == True:
            files = [os.path.join(root, file) for root, dirs, files in os.walk(self.module_path) for file in files if file.endswith('.json')]
            for file_name in files:
                gdf = MFDesign()
                gdf.update( file_name )
        else:
            if os.path.exists( self.full_name ):
                gdf = MFDesign()
                gdf.update( self.full_name )
            else:
                err("File not found: " + self.file_name)
                info("Did you mean: 'update recursive'?")

                
    def on_add(self):
        '''|
        | Command 'add' adds an interface to the .json file and updates the HW module design files
        |________'''
        interface_type = self.arguments[0]
        
        gdf = MFDesign()
        gdf.initialize( self.full_name )

        found = self.check_name( gdf, self.opt_Name )

        if found:
            err("Can not add - interface with the same name exists: " + self.opt_Name)
            exit(0)

        if interface_type == 'HSD':
            gdf.interfaces.append({'push': self.opt_Push, 'direction': self.opt_Direction, 'data': self.opt_Data, 'type': interface_type, 'name': self.opt_Name})

        elif interface_type == 'Bus':
            gdf.interfaces.append({'interfaces': self.opt_BusType, 'type': interface_type, 'name': self.opt_Name})

        elif interface_type == 'Parameter':
            gdf.parameters.append({'value': self.opt_ParValue, 'name': self.opt_Name})

        elif interface_type == 'STAvln':
            gdf.interfaces.append({'direction': self.opt_Direction, 'width': self.opt_Data, 'type': interface_type, 'name': self.opt_Name})

        else: # this should not happen
            err("Unknown type: " + interface_type)
            exit(0)
            
        gdf.overwrite = True
        print_json_file( gdf )

        gdf.update( self.full_name )
        

    def on_remove(self):
        '''|
        | Command 'remove' removes an interface from the .json file and updates the HW module design files
        |________'''
        interface_name = self.arguments[0]

        gdf = MFDesign()
        gdf.initialize( self.full_name )

        found = self.check_name( gdf, interface_name )

        if not found:
            err("Name not found: " + interface_name)
            exit(0)

        # Remove Interface
        gdf.interfaces[:] = [value for value in gdf.interfaces if value["name"] != interface_name]
        # Remove Parameter
        gdf.parameters[:] = [value for value in gdf.parameters if value["name"] != interface_name]

        gdf.overwrite = True
        print_json_file( gdf )

        gdf.update( self.full_name )
    
        
    def on_test(self):
        '''|
        | Command 'test' executes the unit tests for the given module.
        | The tests are specified in the corresponding utest*.py file. 
        |________'''
        self.remove_all('.pyc')

        file_name = "utest_" + self.file_name[:-5] + '.py'
        
        if "recursive" in self.arguments:
            cmd = 'nosetests -vsx -w ' + self.module_path + ' -i "test"'

        elif "with-coverage" in self.arguments:
            cmd = 'nosetests -vsx ' + self.module_path + '/' + 'test/' + file_name + \
                  " --with-coverage --cover-erase --cover-html" + " --cover-html-dir=" + self.module_path + "/out/coverage_html"

        elif self.arguments != []: # to run specific test
            cmd = 'nosetests -vsx ' + self.module_path + '/' + 'test/' + file_name + ':Test_' + self.file_name[:-4] + self.arguments[0]

        else:
            cmd = 'nosetests -vsx ' + self.module_path + '/' + 'test/' + file_name
            
        status = os.system(cmd)
        self.status = status % 255 # On Unix: the first byte indicates signals, the second byte - the status
        
        
    def on_convert(self):
        '''|
        | Command 'convert' converts the myhdl RTL description of a module to synthesizable verilog or vhdl.
        |________'''
        self.remove_all('.pyc')

        # TODO: convert verilog and convert vhdl as separate commands
        
        cmd = 'python ' + self.module_path + '/' + self.file_name[:-5] + '.py'
        os.system(cmd)


    def on_clean(self):
        '''|
        | Command 'clean' removes the files, which have been generated as a result of running simulation or conversion to verilog or vhdl.
        |________'''
        OK = True
        recursive = "recursive" in self.arguments

        if not os.path.exists( self.full_name ) and not recursive:
            warn("File not found: " + self.file_name)
            choise = raw_input("Proceed with 'clean recursive'? y/N ")
            OK = (choise == 'Y' or choise == 'y')

        if OK:
            self.remove_all(*['.pyc', '.vcd', '.vhd', '.tvr', '.*~'])
            
            for root, dirs, files in os.walk(self.module_path):
                for file in files:
                    if file.endswith('.v') and 'out' in root: # To avoid deleting .v files in the 'src' directory (vhd?)
                        os.remove(root + '/' + file)

                for dir in dirs:
                    if dir == "coverage_html":
                        shutil.rmtree(root + '/' + dir)


    def on_delete(self):
        '''|
        | Command 'delete' removes all files and directories from the module's directory tree. It keeps only the .json file.
        |________'''
        choise = raw_input("Delete design? y/N ")
        OK = (choise == 'Y' or choise == 'y')

        if OK:
            cmd = 'cp ' + self.module_path + '/' + self.file_name + ' ~/' + self.file_name
            os.system(cmd)

            cmd = 'rm -rf ' + self.module_path + '/*'
            os.system(cmd)

            cmd = 'mv ~/' + self.file_name + " " + self.module_path + '/' + self.file_name
            os.system(cmd)


    def on_webdoc(self):
        webbrowser.open_new_tab("http://hnikolov.github.io/pihdf_doc")


    def on_version(self):
        info("myhdl     : " + myhdl.__version__)
        info("myhdl_lib : " + myhdl_lib.__version__)
        info("pihdf     : " + pihdf.__version__)
        info("module    : " + "0.1.1")


    # =======================================================================
    def remove_all(self, *args):
        '''|
        | 'args' is a list of file extensions. This function removes all files with the
        | given extension in all sub-directories of 'module_path'
        |________'''
        for root, dirs, files in os.walk(self.module_path):
            for file in files:
                for extension in args:
                    if file.endswith(extension):
                        os.remove(root + '/' + file)


    def check_path_and_create_json(self, file_name):
        '''|
        | Checks if the new module directory and the corresponding .json file exists in the provided path.
        | If not, this function creates the directory and a default .json file (containing only Reset and Clock interfaces).
        | In this way, a new module design (directory structure and files) can always be initialized correctly.
        |________'''
        dirname, filename = os.path.split(file_name)

        if not os.path.exists( dirname ):
            info("Target module path does not exist. Creating a directory...")
            os.makedirs( dirname )

        if not os.listdir( dirname ): # empty directory
            info("Target module .json file does not exist. Creating a default file...")

        if len(os.listdir( dirname )) > 1:
            err("The target module directory is not empty. Use command 'delete' before you start again. Aborting...")
            exit(0)

        # Create a default .json file
        if not os.path.isfile( file_name ):
            s = StrBuilder()
            s.indent()
            s += '{\n'
            s += s.indent() + '"design":\n'
            s += '{\n'
            s += s.indent() + '"name": "' + filename[:-5] + '",\n'
            s += '"interfaces":\n'
            s += '[\n'
            s.indent()
            s += '{ "name": "rst", "type": "Reset", "active": "1" },\n'
            s += '{ "name": "clk", "type": "Clock" }\n'
            s += s.dedent() + ']\n'
            s += s.dedent() + '}\n'
            s += s.dedent() + '}\n'

            s.write( file_name )

        
    def check_name(self, gdf, name ):
        '''|
        | Used by commands 'add' and 'remove'
        |________'''        
        for value in gdf.interfaces:
            if value["name"] == name:
                return True
        for value in gdf.parameters:
            if value["name"] == name:
                return True
        return False
