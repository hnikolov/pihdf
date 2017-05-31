import traceback
import math

from myhdl import *
from myhdl_lib import pipeline_control


class RegFile:
    '''|
    | TODO
    |________'''    

    def __init__(self):
        self.ls = []
        self.ls_addr = []

    def get_instance_name(self):
        '''|
        | Creates a unique name to be associated with an instantiated register
        |________'''    
        name = []
        i = -4

        while True:
            (filename,line_number,function_name,text)=traceback.extract_stack()[i]
            i -= 1

            if function_name=="gen":  # Skip the gen functions
                continue

            tmp_str = text.split()

            if tmp_str[0] in ['h', '_top', 'sim_dut']: # Extra levels to filter in case of cosimulation
                break

            name.append(tmp_str[0])

        name.reverse()

        return '.'.join(name)


    def get_interface(self, tp, width, sname):
        '''|
        | Creates and returns interface signals. Stores the interface in self.ls
        |________'''    

        # This name represents the instantiation hierarchy
        inst_name = self.get_instance_name()
        iname = sname if inst_name == "" else sname + '@' + inst_name

        re = Signal(bool(0))
        rd = Signal(intbv(0)[width:])
        we = Signal(bool(0))
        wd = Signal(intbv(0)[width:])

        if tp == "wg":
            for i in self.ls:
                if sname == i["iname"]:
                    we = i["we"]
                    wd = i["wd"]
                    break
            else:
                self.ls.append({"iname": sname, "type":tp, "width":width, "re":re, "rd":rd, "we":we, "wd":wd})
        else:
            self.ls.append({"iname": iname, "type":tp, "width":width, "re":re, "rd":rd, "we":we, "wd":wd})

        if tp == "ro":
            return re, rd
        elif tp in ["wo", "wg"]:
            return we, wd
        elif tp == "rw":
            return re, rd, we, wd
        else:
            print "Unknown register type: {}".format(tp)


    def print_register_list(self, filename):
        '''|
        | Print the list of registers
        |________'''    
        s = "-----------\n"
        s += "Register list:\n"
        s += "-----------\n"
        for i,j in enumerate(self.ls):
            s += "{:3} : [{}:] {}\n".format(i, j['width'], j['iname'])
        s += "-----------\n"

        print s

        if filename != "":
            tmpFile = open(filename, 'w')
            tmpFile.write(s)
            tmpFile.close()


    def create_address_map(self, BUS_DWIDTH, filename):
        '''|
        | Creates an address map from all interfaces stored in self.ls
        |________'''    

        self.print_register_list(filename)

        START_ADDRESS = 0
        ls_addr = []
        addr_lo = addr_hi = START_ADDRESS

        # Map the registers into the address space. The code supports 'big' registers
        for r in self.ls:
            num_words = int(math.ceil(float(r["width"])/BUS_DWIDTH))
            addr_hi = addr_lo + num_words
            ls_addr.append(range(addr_lo, addr_hi))
            addr_lo = addr_hi

        # Print a dict "reg":addr into a .py file
        addr = {}
        for i,addr_list in enumerate(ls_addr):
            hier_name = self.ls[i]["iname"]
            simple_name = hier_name[0:hier_name.find("@")] # Temporary use reg simple name, not hierarchical name, until we fix hierarchy
            addr[simple_name] = addr_list[0]
            
        with open("mem_map.py", 'w') as theFile:
            theFile.write("addr = " + str(addr))

        print "------------"
        print "Address map:"
        print "------------"
        for i,al in enumerate(ls_addr):
            for j,a in enumerate(al):
                lo = j*BUS_DWIDTH
                hi = min((j+1)*BUS_DWIDTH, self.ls[i]["width"])
                print "{:3} : [{:3}:{:3}] {}".format(a, hi, lo, self.ls[i]["iname"])
        print "------------"
        
        self.ls_addr = ls_addr
