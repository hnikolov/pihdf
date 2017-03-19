"""
pihdf stimuli scheduling for humans.

... that uses the builder pattern for configuration. 
... using a simple, human-friendly syntax.

Inspired by Daniel Bader: github.com/dbader/schedule
Inspired by Addam Wiggins' article "Rethinking Cron" [1] and the
"clockwork" Ruby module [2][3].

Features:
    - 

Keywords:
    - drive
    - capture
    - after
    - after_every
    - stimuli
    - start_at
    - samples
    - with_gaps
    
Usage (in other python modules):
    import pschedule

    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]
    
    pschedule.drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)
    pschedule.drive(stim_rx_2).samples([2, 4, 7]).after(stim_rx_1).samples([1, 4, 8])    
    
    print pschedule.get('rx_1')
    print pschedule.get('rx_2')
    # or
    pschedule.print_schedules()    

    pschedule.print_configurations()
    pschedule.clear_configurations()
"""

import traceback
from pihdf import Testable

class Scheduler(object):
    '''|
    | Objects instantiated by the `Scheduler` are factories to create configurations.
    |________'''
    def __init__(self):
        self.configs = []


    def add(self, stimuli):
        '''|
        | Add a new configuration.
        |
        | return: An empty config
        |________'''
        config = Config( stimuli )
        self.configs.append( config )
        return config

    def clear_configs(self):
        self.configs = []
        
    def clear_schedules(self):
        '''|
        | Clear all derived schedules
        |________'''
        for config in self.configs:
            config.cond_list = []

    def print_configurations(self):
        '''|
        | Prints the configurations of all stimuli
        |________'''
        if self.configs == []:
            print "Nothing to print"

        for config in self.configs:
            config.print_configuration()
        
    def determine_schedule(self, i):
        self.configs[i].determine_schedule()
        
    def print_schedule(self, i):
        self.configs[i].print_cond_list()
        

class Config(object):
    '''|
    |
    |________'''
    def __init__(self, stimuli_list):
        self._stimuli_len     = len(stimuli_list)
        # Find name after 'drive(' and 'capture(', i.e., after the first '('
        self._name               = self.find_name_after('(', lo=-5)
        self._name_after         = None
        self._after_every_len    = None
        self._after_len          = None
        self._stimuli            = None
        self._start_at           = None
        self._samples_list       = None
        self._samples_after_list = None
        self._with_gaps          = None
        
        self.cond_list           = []
        
        self.schedule_type       = None # Set by determine_schedule()
                
        self.handle = {
            'sch_gen_1' : self.sch_gen_1,
            'sch_gen_2' : self.sch_gen_2,
            'sch_gen_3' : self.sch_gen_3,
            'sch_gen_4' : self.sch_gen_4,
            'sch_gen_5' : self.sch_gen_5,
            'sch_gen_6' : self.sch_gen_6,
            'sch_gen_7' : self.sch_gen_7,
            'sch_gen_8' : self.sch_gen_8,
            'sch_gen_9' : self.sch_gen_9
        }
        
        

    def condition_generator(self):
        if self.schedule_type is None:
            self.determine_schedule()
        return self.handle[ self.schedule_type ]()
        
    
    def isPresent(self):
        return self.schedule_type != None
     
        
    def find_name_after(self, sname, lo):
        (filename,line_number,function_name,text)=traceback.extract_stack()[lo]
        idx = text.find(sname)

        if idx != -1:
            text = text[idx:]
            tmp_txt = text[len(sname):text.find(')')].strip()
            # remove self.stim_, self.res_ and self.ref_ if present
            tmp_txt = self._remove_prefix( tmp_txt, 'self.')
            tmp_txt = self._remove_prefix( tmp_txt, 'stim_')
            tmp_txt = self._remove_prefix( tmp_txt, 'res_')
            return    self._remove_prefix( tmp_txt, 'ref_')

        return "NO NAME FOUND"
        
    def _remove_prefix(self, sname, prefix):
        #TODO: sname = sname[len(prefix):] if sname.startswith(prefix) else sname
        return sname[len(prefix):] if sname.startswith(prefix) else sname

    def after_every(self, stimuli_list):
        if self._after_len is not None:
            print 'In "after_every": "after" not None. Use either "after_every" or "after"'
            exit()
            
        self._after_every_len = len(stimuli_list)
        self._name_after = self.find_name_after('every(', lo=-3)        
        
        return self

    def after(self, stimuli_list):
        if self._after_every_len is not None:
            print 'In "after": "after_every" not None. Use either "after_every" or "after"'
            exit()

        self._after_len = len(stimuli_list)
        self._name_after = self.find_name_after('after(', lo=-3)

        return self

    def stimuli(self, stimuli_number):
        self._stimuli = stimuli_number
        return self

    def start_at(self, stimuli_number):
        self._start_at = stimuli_number
        return self
        
    def samples(self, list_of_samples):
        if self._name_after is None: # See examples sch 7 and 8
            self._samples_list = list_of_samples 
        else:
            self._samples_after_list = list_of_samples
        return self
        
    def with_gaps(self, ipg):
        self._with_gaps = ipg
        return self
        
    def print_configuration(self):
        print '-- Interface name:',     self._name, '--------------------------'        
        print '   stimuli length:',     self._stimuli_len       
        print '   name_after:',         self._name_after       
        print '   after_every_len: ',   self._after_every_len   
        print '   after_len: ',         self._after_len         
        print '   stimuli: ',           self._stimuli       
        print '   start_at:',           self._start_at      
        print '   samples_list:',       self._samples_list      
        print '   samples_after_list:', self._samples_after_list
        print '   with_gaps',           self._with_gaps     
        print ''

    def print_cond_list(self):
        print self.cond_list

    def get(self):
        if self.cond_list == []:
            self.determine_schedule()
            
        return self.cond_list 
        # TODO: return self.condition_generator()
        
    # TODO: Basic consistency check of a configuration
    def check(self):
        # after + samples; after_every + !samples
        # len samples == len samples_after
        # TODO: in case of 'res_if', len=0
        # samples start from 1
        pass
                

    def determine_schedule(self):
        # TODO
        if self._with_gaps is not None:
            print "INFO: with_gaps not supported yet"
            return
            
        if self._start_at > 0 and self._after_len is not None:
            # drive(stim_rx_2).after(stim_rx_1).start_at(5)
            self.sch_3()
            self.schedule_type = 'sch_gen_3'
            
        else:            
            if self._start_at == 0 and self._stimuli is None:
                # drive(stim_rx_2).after_every(stim_rx_1).start_at(0)
                self.sch_9()
                self.schedule_type = 'sch_gen_9'
                
            elif self._start_at > 0 and self._stimuli is None:
                # drive(stim_rx_2).after_every(stim_rx_1).start_at(3)
                self.sch_2()
                self.schedule_type = 'sch_gen_2'

            elif self._stimuli > 0:                 
                if self._start_at == 0:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0)
                    self.sch_5()
                    self.schedule_type = 'sch_gen_5'
                        
                elif self._start_at > 0:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)
                    self.sch_6()
                    self.schedule_type = 'sch_gen_6'
                                
                else:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3)
                    self.sch_4()
                    self.schedule_type = 'sch_gen_4'
                    
            elif self._samples_list is None and self._samples_after_list is not None:
                # drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9])
                self.sch_7()
                self.schedule_type = 'sch_gen_7'
                
            elif self._samples_list is not None and self._samples_after_list is not None:
                # drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9])
                self.sch_8()
                self.schedule_type = 'sch_gen_8'
                
            else:
                # drive(stim_rx_2).after_every(stim_rx_1)                
                self.sch_1()
                self.schedule_type = 'sch_gen_1'
                                

    def sch_1(self): # drive(stim_rx_2).after_every(stim_rx_1) t2
        for i in range(self._stimuli_len):
            self.cond_list.append( (i, (self._name_after, i) ) )

    def sch_2(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(3) t3
        for i in range(self._stimuli_len):
            sample = (self._start_at - 1) + i
            self.cond_list.append( (i, (self._name_after, sample ) ) )
            if sample >= self._after_every_len - 1:
                return
            
    def sch_3(self): # drive(stim_rx_2).after(stim_rx_1).start_at(5) t4 
        self.cond_list.append( (0, (self._name_after, self._start_at-1) ) )
        
    def sch_4(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3) t5
        for i in range(self._stimuli_len):
            sample = (self._stimuli - 1) + (i * self._stimuli)
            self.cond_list.append( (i, (self._name_after, sample) ) )
            if sample >= self._after_every_len - self._stimuli:
                return
            
    def sch_5(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0) t6
        for i in range(self._stimuli_len):
            src_sample = i + 1
            sample = (self._stimuli - 1) + (i * self._stimuli)
            self.cond_list.append( (src_sample, (self._name_after, sample) ) )
            if sample >= self._after_every_len - self._stimuli:
                return
            
    def sch_6(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3) t7
        for i in range(self._stimuli_len):
            sample = (self._start_at - 1) + (i * self._stimuli)    
            self.cond_list.append( (i, (self._name_after, sample) ) )
            if sample >= self._after_every_len - self._stimuli:
                return
            
    def sch_7(self): # drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9]) t8
        for i, s in enumerate(self._samples_after_list):
            self.cond_list.append( (i, (self._name_after, s-1) ) )
            
    def sch_8(self): # drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9]) t9
        for i, s in zip(self._samples_list, self._samples_after_list):
            self.cond_list.append( (i-1, (self._name_after, s-1) ) )
            
    def sch_9(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(0) t10
        for i in range(1, self._stimuli_len):
            self.cond_list.append( (i, (self._name_after, i-1) ) )
            
#-- Generators -----------------------------------------------------------------------------

    def sch_gen_1(self): # drive(stim_rx_2).after_every(stim_rx_1) t2
        for i in range(self._stimuli_len): # TODO: Can be infinite
            yield (i, (self._name_after, i))

    def sch_gen_2(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(3) t3
        for i in range(self._stimuli_len):
            sample = (self._start_at - 1) + i
            yield (i, (self._name_after, sample))
            if sample >= self._after_every_len - 1:
                break
            
    def sch_gen_3(self): # drive(stim_rx_2).after(stim_rx_1).start_at(5) t4 
        yield (0, (self._name_after, self._start_at-1) )
        
    def sch_gen_4(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3) t5  
        for i in range(self._stimuli_len):
            sample = (self._stimuli - 1) + (i * self._stimuli)
            yield (i, (self._name_after, sample))
            if sample >= self._after_every_len - self._stimuli:
                break
            
    def sch_gen_5(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0) t6
        for i in range(self._stimuli_len):
            src_sample = i + 1
            sample = (self._stimuli - 1) + (i * self._stimuli)
            yield (src_sample, (self._name_after, sample))
            if sample >= self._after_every_len - self._stimuli:
                break
            
    def sch_gen_6(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3) t7
        for i in range(self._stimuli_len):
            sample = (self._start_at - 1) + (i * self._stimuli)    
            yield (i, (self._name_after, sample))
            if sample >= self._after_every_len - self._stimuli:
                break
            
    def sch_gen_7(self): # drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9]) t8
        for i, s in enumerate(self._samples_after_list):
            yield (i, (self._name_after, s-1) )
            
    def sch_gen_8(self): # drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9]) t9
        for i, s in zip(self._samples_list, self._samples_after_list):
            yield (i-1, (self._name_after, s-1) )
            
    def sch_gen_9(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(0) t10
        for i in range(1, self._stimuli_len):
            yield (i, (self._name_after, i-1) )
            


# ----------------------------------------------------------------------------------
# The following methods are shortcuts for not having to create a Scheduler instance
# ----------------------------------------------------------------------------------

default_scheduler = Scheduler()


def drive( stimuli ): # TODO: Should be the same for 'drive' and 'capture'
    """
    ... with the default module scheduler.

    :return: The default :obj:`Scheduler` instance
    """
    return default_scheduler.add( stimuli )

def capture( stimuli ): # TODO: Should be the same for 'drive' and 'capture'
    return default_scheduler.add( stimuli )

def get( name ):
    for config in default_scheduler.configs:
        if name == config._name:
            return config.get()
    return []

def get_condition_generator( name ):
    for config in default_scheduler.configs:
        if name == config._name:
            return config.condition_generator()


def _get( idx ):
    return default_scheduler.configs[idx].get()

def clear_configurations():
    default_scheduler.clear_configs()
    
def clear_schedules():
    default_scheduler.clear_schedules()
    
def print_configurations():
    default_scheduler.print_configurations()

def get_schedule(i):
    default_scheduler.determine_schedule(i)
    default_scheduler.print_schedule(i)

def print_schedules():
    default_scheduler.clear_schedules()
    for i in range(len(default_scheduler.configs)):
        default_scheduler.determine_schedule(i)
        default_scheduler.print_schedule(i)

def use_generator():
    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]

    drive(stim_rx_2).after_every(stim_rx_1) # test_002

    default_scheduler.determine_schedule(0)

    c = default_scheduler.configs[0].condition_generator()
    if c is not None:
        condition = 'None'
        for _ in range(7):
            try:
                condition = c.next()
            except StopIteration:
                pass

            print condition # Iterations 6 and 7 print the last (valid) condition
    else:
        print "Generator is None"





class SchedBuilder():
    def __init__(self, tb):
        assert isinstance(tb, Testable), "Class SomeScheduler must be initialized with a testbench instance"
        self.testbench = tb

        self.iface = None
        self.index = None
        self.cond = []
        self.delay = None

    def _get_conditions(self, iface_name, index):
        """ Finds the cond_* list that will to be updated """
        cond_list = self.testbench.tst_data.get("cond_" + iface_name)
        assert cond_list is not None, 'Interface "{}" not found. Available interfaces: {}'.format(iface_name, self.testbench.tst_data.keys())
        self.iface = cond_list
        self.index = index
        return self

    drive = _get_conditions
    capture = _get_conditions

    def after(self, iface_name, index):
        """ Adds another condition to the current condition term """
        self.cond.append((iface_name, index))
        return self

    def gap(self, clock_cycles):
        """ Adds gap to the current condition term """
        self.delay = clock_cycles
        return self

    def end(self):
        """ Constructs a condition tuple and adds it the the cond_* list"""
        # This can be also a object deleter
        if self.delay is None:
            self.iface.append((self.index, self.cond))
        else:
            self.iface.append((self.index, self.cond, self.delay))
        self.iface = None
        self.index = None
        self.cond = []
        self.delay = None

    def __str__(self):
        """ Attempt for a schedule printer"""
        td = self.testbench.tst_data
        rd = self.testbench.ref_data

        # Dictionary : all_cond[port_name] = cond_*
        all_cond = {s[len("cond_"):]:td[s] for s in td.keys() if s.startswith("cond_")}
        del all_cond["sim_end"]
        # Dictionary: all_lengths[port_name] = len(stim_* | ref_*)
        all_lengths = {s[len("stim_"):]:len(td[s]) for s in td.keys() if s.startswith("stim_")}
        all_lengths.update({s:len(rd[s][0]) for s in rd.keys()})
        # Crosscheck
        assert set(all_cond.keys()) == set(all_lengths.keys())
        # Just to always use the names in the same order
        names = all_cond.keys() # TODO: ordered dict ?
        max_len = max(all_lengths.values())
        all_cntr = dict(zip(names, len(names)*[0]))

        fmt_str = "{:>6}   " + "".join(["{:>15}   " for n in names]) + "\n"
        s = ""
        s += fmt_str.format("", *len(names)*["-----"])
        s += fmt_str.format("", *names)
        s += fmt_str.format("", *[all_lengths[n] for n in names])
        s += fmt_str.format("", *len(names)*["-----"])

        class CondProcessor():
            def __init__(self, name, counters, conditions, lengths):
                self.my_name = name
                self.my_length = lengths[name]
                self.counters = counters
                self.conditions = conditions
                self.lengths = lengths
                self.increment = False
                self.done = False

            def evaluate(self):
                for condition in self.conditions[self.my_name]:
                    self.increment = False
                    my_index = condition[0]
                    my_cond = condition[1]
                    my_gap = condition[2] if len(condition) > 2 else None
                    while self.counters[self.my_name] < my_index:
                        self.increment = True
                        yield self.counters[self.my_name]
                    if self.counters[self.my_name] > my_index:
                        continue
                    for cond in my_cond:
                        if_name  = cond[0]
                        if_index = cond[1]
                        while self.counters[if_name] <= if_index:
                            self.increment = False
                            yield "?{:}[{:}]".format(if_name, if_index)
                    if my_gap is not None:
                        self.increment = False
                        yield "?gap({:})".format(my_gap)
                    self.increment = True
                    yield self.counters[self.my_name]
                while self.counters[self.my_name] < self.my_length:
                    self.increment = True
                    yield self.counters[self.my_name]
                self.done = True
                self.increment = False
                while True:
                    yield "."

            def update(self):
                if self.increment:
                    self.counters[self.my_name] += 1

            def is_done(self):
                return self.done

        procs = [CondProcessor(n, all_cntr, all_cond, all_lengths) for n in names]

        gen = [x.evaluate() for x in procs]

        for i in range(max_len*len(names)):
            if all([x.is_done() for x in procs]):
                break
            ss = [x.next() for x in gen]
            s += fmt_str.format(i, *ss)
            for x in procs:
                x.update()

        return s.format(*names)


# Some usage examples, tests
if __name__ == '__main__':
    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]
    
    print_configurations() # Nothing to print
    
#    drive(stim_rx_2).after_every(stim_rx_1).after(stim_rx_1)                   # Detect ERROR: wrong usage
#    drive(stim_rx_2).after(stim_rx_1).start_at(5).after_every(stim_rx_1)       # Detect ERROR: wrong usage
    drive(stim_rx_2).after_every(stim_rx_1)                                     # test_002            
    drive(stim_rx_2).after_every(stim_rx_1).start_at(3)                         # test_003
    drive(stim_rx_2).after(stim_rx_1).start_at(5)                               # test_004 (Enable after 5)
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3)                          # test_005
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0)              # test_006 (1st sample after reset)
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)              # test_007
    drive(stim_rx_2).after(stim_rx_1).samples([3, 7, 8])                        # test_008 (1 after 3, 2 after 7, 3 after 8)
    drive(stim_rx_2).samples([2, 4, 7]).after(stim_rx_1).samples([1, 4, 8])     # test_009 (2 after 1, 4 after 4, 7 after 8)

    drive(stim_rx_2).with_gaps(4) # TODO: not supported yet
    
    # Pink-Ponk
    drive(stim_rx_2).after_every(stim_rx_1).start_at(0) # start_at(0) == drive first sample after reset w/o condition
    drive(stim_rx_1).after_every(stim_rx_2)
    # ---------
    
    print_configurations()
    
    print_schedules()    
    
    clear_configurations()
    print_configurations()
    
    use_generator()
    
