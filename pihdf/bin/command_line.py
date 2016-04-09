"""|
| module: a convenient front-end tool of pihdf
|________

Usage:
    module <command>
    module MPATH <command> [<args> ...] [options]

Main argument:
    MPATH             Specifies a HW module root directory

Commands not using MPATH:
    help              Prints this help message
    webdoc            Opens the web documentation
    version           Prints the version of myhdl, pihdf, and module
  
Other commands:
    new               create a new module project from a <module_name>.json file
    add               add a new top-level interface or parameter
    remove            remove a top-level interface or parameter
    update            re-generate the files of a module
    test              execute the unit tests for the specified module. Optional test name can be provided
    convert           convert the myhdl description of a module to verilog
    clean             remove temporary files generated in the module's directory tree
    delete            delete all files and directories from the module's directory tree; keep the .json file

Arguments can/are used with the following commands:
    update  [recursive]
    convert [verilog]       | [vhdl]
    test    [<test_name>    | [recursive]       [with-coverage]]
    add     (interface_type | parameter_type)   <options>
    remove  (interface_name | parameter_name)

Options:
    The following options are used with command 'add'
   -n <name>           Instance name             [default: None]
   -d <direction>      Can be 'IN' or 'OUT'      [default: None]
   -p <push>           Push-type of interface    [default: False]
   -v <value>          Parameter value           [default: None]
   -i <bus_name>       The set of bus interfaces [default: None]
   -w <width/fields>   Interface fields or width [default: None]
   
More information is available at
    http://hnikolov.github.io/pihdf_doc    Use <CTRL + mouse click> to follow the link

"""
from docopt import docopt

from CommandChecker import CommandChecker
from CommandHandler import CommandHandler


def main():
    arguments = docopt(__doc__)

    #if arguments["help"] == True and arguments["<command>"] != None: # Consider if needed also: module help [<command>]; check also docopt git help example
    if arguments["<command>"] == 'help':
        print __doc__
    else:
        cc = CommandChecker(  arguments   )
        ch = CommandHandler( cc.arguments )
        print "done"
        exit(ch.status)
