import mylog


class Testable():
    '''|
    | The base class for unit-testing
    |________'''

    def __init__(self):

        self.BEH = 0
        self.RTL = 1
        self.VRG = 2

        self.dut_params = {}
        self.models = {}
        self.tb_config = {}

        self.checkfiles = False
        self.err = 0
        self.verbose = False


    def dict2string(self, conf):
        '''|
        | Converts test configuration (dictionary) into a string
        | Also, updates the test configuration by adding all default items if omitted during test creation
        |________'''
        # Default configuration
        configuration = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False, "ipgi":0, "ipgo":0}

        # Update the configuration with the actual configuration
        for key,value in conf.iteritems():
            configuration[key] = value

        conf.update(configuration)

        # Convert to string
        s = ''
        for key,value in configuration.iteritems():
            if self.verbose: # Can be set in each test
                s += key + " = " + str(value) + ", "
            else:
                if str(value) != "False":
                    if str(value) == "True":
                        s += key + ", "
                    elif value != 0 and str(value) != "auto":
                        s += key + " = " + str(value) + ", "
                    
        return s[:-2]


    def params2string(self, params):
        '''|
        | Converts parameter information (dictionary) into a string
        |________'''
        s = ''
        for key,value in params.iteritems():
            s += key + " = " + str(value) + ", "

        return s[:-2]        


    def impl2string(self, conf):
        '''|
        | Converts a dictionary (containing implementation information) into a string
        |________'''
        impl     = [self.BEH, self.RTL, self.VRG]
        impl_str = ['BEHAVIOR', 'MyHDL_RTL', '(external) VERILOG']
        s = ''
        for key,value in conf.iteritems():
            if len(conf) == 1:
                return impl_str[value]
            
            if value not in impl:
                mylog.err(key + ": Wrong implementation model selected: (" + str(value) + ")! Exit...")
                exit()
            s += key + " = " + impl_str[value] + ", "
        return s[:-2]


    def check_config(self, cname):
        '''|
        | Check test configuration
        | Determine the end-of-simulation conditions: len of stim_ and ref_ lists
        |________'''
        mylog.info(cname + ": " + self.impl2string(self.models))

        conf_str = self.dict2string(self.tb_config)
        if conf_str != '':
            mylog.info("Configuration: " + conf_str)

        if self.dut_params != {}:
            mylog.info("DUT parameters: " + self.params2string(self.dut_params))

        mty_stim_list = True
        stim_not_present = True
        for key,val in self.tst_data.iteritems():
            if "stim" in key:
                stim_not_present = False
                if val != [] and "file" in val[0]:
                    num_payloads = sum(1 for line in open(val[0]["file"]))
                    self.cond_sim_end[key[5:]] = num_payloads
                else:
                    self.cond_sim_end[key[5:]] = len(val)

                if self.cond_sim_end[key[5:]] > 0:
                    mty_stim_list = False
                
        if stim_not_present or mty_stim_list:
            mylog.info("No stimuli provided")
            
        no_ref_data = True
        for key,val in self.ref_data.iteritems():
            if val[0] != [] and "file" in val[0][0]:
                num_payloads = sum(1 for line in open(val[0][0]["file"]))
                self.cond_sim_end[key] = num_payloads
            else:
                self.cond_sim_end[key] = len(val[0])

            if self.cond_sim_end[key] > 0:
                no_ref_data = False

        # To avoid endless simulation
        if self.tb_config["simulation_time"] == "auto" and (stim_not_present or mty_stim_list) and no_ref_data:
            self.tb_config["simulation_time"] = 5
            mylog.warn("Simulation time ca not be determined! Selecting a constant simulation time.")


    def check_results(self):
        '''|
        | Call different check function depending on the configuration
        |________'''
        if self.checkfiles:
            self.compare_ref_with_res_files()
        else:
            if self.err > 0:
                self.compare_almost_ref_with_res()
            else:
                self.compare_ref_with_res()

        
    def compare_ref_with_res(self):
        '''|
        | Check the results
        |________'''
        for name, (ref,res) in self.ref_data.items():
            assert( len(ref)==len(res)), "\tCOMPARE ERROR: Length mismatch for \"{:}\". Detected lengths: \n\t len(expected)={:} \n\t len(detected)={:} \n\t".format(name, len(ref), len(res))
            # check fields
            for i in range(len(ref)):
                for fld in ref[i].keys():
                    if fld=="payload":
                        exp_pld = ref[i]["payload"].encode("hex") if isinstance(ref[i]["payload"], str) else ref[i]["payload"]
                        det_pld = res[i]["payload"].encode("hex") if isinstance(res[i]["payload"], str) else res[i]["payload"]
                        assert (exp_pld==det_pld), "\tCOMPARE ERROR: \"{:}\" payload #{:}: Payload does not match: \n\t expected={:} \n\t detected={:}".format(name, i+1, exp_pld, det_pld)
                    else:
                        assert (ref[i][fld]==res[i][fld]), "\tCOMPARE ERROR: \"{:}\" fields #{:}: Field \"{:}\" does not match: expected={:} detected={:}".format(name, i, fld, ref[i][fld], res[i][fld])


    #def compare_comp_ref_with_res(self):
        #'''|
        #| TODO: Check the results (complex numbers)
        #|________'''
        #for name, (ref,res) in self.ref_data.items():
            #assert( len(ref)==len(res)), "\tCOMPARE ERROR: Length mismatch for \"{:}\". Detected lengths: \n\t len(expected)={:} \n\t len(detected)={:} \n\t".format(name, len(ref), len(res))
            ## check fields
            #for i in range(len(ref)):
                #for fld in ref[i].keys():
                    #if fld=="payload":
                        #exp_pld = ref[i]["payload"].encode("hex") if isinstance(ref[i]["payload"], str) else ref[i]["payload"]
                        #det_pld = res[i]["payload"].encode("hex") if isinstance(res[i]["payload"], str) else res[i]["payload"]
                        ##self.assertAlmostEqual(exp_pld.real, det_pld.real, 3)
                        ##self.assertAlmostEqual(exp_pld.imag, det_pld.imag, 3)
                        #assert (exp_pld==det_pld), "\tCOMPARE ERROR: \"{:}\" payload #{:}: Payload does not match: \n\t expected={:} \n\t detected={:}".format(name, i+1, exp_pld, det_pld)
                    #else:
                        #assert (ref[i][fld]==res[i][fld]), "\tCOMPARE ERROR: \"{:}\" fields #{:}: Field \"{:}\" does not match: expected={:} detected={:}".format(name, i, fld, ref[i][fld], res[i][fld])


    def compare_almost_ref_with_res(self):
        '''|
        | Check the results (tolerate a difference within an error)
        |________'''
        #err = 0.005 # 0.5%
        for name, (ref,res) in self.ref_data.items():
            assert( len(ref)==len(res)), "\tCOMPARE ERROR: Length mismatch for \"{:}\". Detected lengths: \n\t len(expected)={:} \n\t len(detected)={:} \n\t".format(name, len(ref), len(res))
            # check fields
            for i in range(len(ref)):
                for fld in ref[i].keys():
                    if fld=="payload":
                        exp_pld = ref[i]["payload"].encode("hex") if isinstance(ref[i]["payload"], str) else ref[i]["payload"]
                        det_pld = res[i]["payload"].encode("hex") if isinstance(res[i]["payload"], str) else res[i]["payload"]

                        gt = exp_pld if exp_pld > det_pld else det_pld
                        tm = abs(exp_pld - det_pld)
                        df = tm/float(gt)
                        assert (df <= self.err), "\tCOMPARE ERROR: \"{:}\" payload #{:}: Payload difference too much: \n\t expected={:} \n\t detected={:} \n\t difference={:} (> {:})".format(name, i+1, exp_pld, det_pld, df, self.err)

                    else:
                        exp_pld = ref[i][fld]
                        det_pld = res[i][fld]
                        gt = exp_pld if exp_pld > det_pld else det_pld
                        tm = abs(exp_pld - det_pld)
                        df = tm/float(gt)
                        assert (df <= self.err), "\tCOMPARE ERROR: \"{:}\" fields #{:}: Field \"{:}\" difference too much: expected={:} detected={:} \n\t difference={:} (> {:})".format(name, i+1, exp_pld, det_pld, df, self.err)

                        
    def compare_ref_with_res_files(self):
        '''|
        | Check the results from files
        |________'''
        for name, (ref,res) in self.ref_data.items():
            try:
                with open(ref[0]["file"], "rb") as expfile, open(res[0]["file"], "rb") as resfile:
                    linesref = expfile.readlines()
                    linesres = resfile.readlines()
                    assert(len(linesref)==len(linesres)), "\tCOMPARE ERROR: Length mismatch for \"{:}\". Detected lengths: \n\t len(expected)={:} \n\t len(detected)={:} \n\t".format(name, len(linesref), len(linesres))
                    k=1
                    for lineref, lineres in zip(linesref, linesres):
                        assert (lineref.strip()==lineres.strip()), "\tCOMPARE ERROR: \"{:}\" payload #{:}: Payload does not match: \n\t expected={:} \n\t detected={:}".format(name, k, lineref.strip(), lineres.strip())
            except IOError:
                mylog.err("Compare reference with result files: File not found")
                