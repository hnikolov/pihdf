"""
pihdf stimuli scheduling for humans.

... that uses the builder pattern for configuration. 
... using a simple, human-friendly syntax.

Inspired by Daniel Bader: github.com/dbader/schedule
Inspired by Addam Wiggins' article "Rethinking Cron" [1] and the
"clockwork" Ruby module [2][3].

Features:
    - 

Usage:
    >>> import schedule
    >>> import time

    >>> def job(message='stuff'):
    >>>     print("I'm working on:", message)

    >>> schedule.every(10).minutes.do(job)
    >>> schedule.every().hour.do(job, message='things')
    >>> schedule.every().day.at("10:30").do(job)

    >>> while True:
    >>>     schedule.run_pending()
    >>>     time.sleep(1)

"""

import traceback
import os, sys

""" Keywords:
    - after_every
    - after
    - stimuli
    - start_at
    - samples
    - with_gaps
"""

class Scheduler(object):
    """
    Objects instantiated by the `Scheduler` are factories to create
    jobs, keep record of scheduled jobs and handle their execution.
    """
    def __init__(self):
        self.configs = []


    def add(self, stimuli):
        """
        Add a new configuration.

        :return: An empty config
        """
        config = Config( stimuli )
        self.configs.append( config )
        return config

    def clear_configs(self):
        self.configs = []
        
    def clear_schedules(self):
        """
        Clear all derived schedules
        """
        for config in self.configs:
            config.cond_list = []

    def print_configurations(self):
        """
        Prints the configurations of all stimuli
        """
        if self.configs == []:
            print "Nothing to print"

        for config in self.configs:
            config.print_configuration()
        
    def determine_schedule(self, i):
        self.configs[i].determine_schedule()
        
    def print_schedule(self, i):
        self.configs[i].print_cond_list()
        

class Config(object):
    """
    """
    def __init__(self, stimuli_list):
        self._stimuli_list  = stimuli_list   
        self._name          = self.find_name_after('drive(', lo=-5)
        self._name_after    = None
        self._after_every   = None
        self._after         = None
        self._stimuli       = None
        self._start_at      = None
        self._samples       = None
        self._samples_after = None
        self._with_gaps     = None
        
        self.cond_list      = []

        self._name = self._remove_prefix( self._name, 'self.stim_' )

    def find_name_after(self, sname, lo):
        (filename,line_number,function_name,text)=traceback.extract_stack()[lo]
        idx = text.find(sname)

        if idx != -1:
            text = text[idx:]
            return text[len(sname):text.find(')')].strip()
            
        return "NO NAME FOUND"
        
    def _remove_prefix(self, sname, prefix):
        #TODO: sname = sname[len(prefix):] if sname.startswith(prefix) else sname
        return sname[len(prefix):] if sname.startswith(prefix) else sname

    def after_every(self, stimuli_list):
        if self._after is not None:
            print 'In "after_every": Use either "after_every" or "after"'
            exit()
            
        self._after_every = stimuli_list
        self._name_after = self.find_name_after('every(', lo=-3)        
        # remove self.stim_ if present
        self._name_after = self._remove_prefix( self._name_after, 'self.stim_')
        
        return self

    def after(self, stimuli_list):
        if self._after_every is not None:
            print 'In "after": Use either "after_every" or "after"'
            exit()

        self._after = stimuli_list
        self._name_after = self.find_name_after('after(', lo=-3)
        # remove self.stim_ if present
        self._name_after = self._remove_prefix( self._name_after, 'self.stim_')

        return self

    def stimuli(self, stimuli_number):
        self._stimuli = stimuli_number
        return self

    def start_at(self, stimuli_number):
        self._start_at = stimuli_number
        return self
        
    def samples(self, list_of_samples):
        if self._after is None:
            self._samples = list_of_samples 
        else:
            self._samples_after = list_of_samples
        return self
        
    def with_gaps(self, ipg):
        self._with_gaps = ipg
        return self
        
    def print_configuration(self):
        print '-- Interface name:', self._name, '--------------------------'        
        print '   stimuli list:',   self._stimuli_list       
        print '   name_after:',     self._name_after       
        print '   after_every: ',   self._after_every   
        print '   after: ',         self._after         
        print '   stimuli: ',       self._stimuli       
        print '   start_at:',       self._start_at      
        print '   samples:',        self._samples       
        print '   samples_after:',  self._samples_after 
        print '   with_gaps',       self._with_gaps     
        print ''

    def print_cond_list(self):
        print self.cond_list

    def get(self):
        if self.cond_list == []:
            self.determine_schedule()
            
        return self.cond_list
        
    # TODO: Basic consistemcy check of a configuration
    def check(self):
        # after + samples; after_every + !samples
        # len samples == len samples_after
        # samples start from 1
        pass
                

    def determine_schedule(self):
        # TODO
        if self._with_gaps is not None:
            print "INFO: with_gaps not supported yet"
            return
            
        if self._start_at > 0 and self._after is not None:
            # drive(stim_rx_2).after(stim_rx_1).start_at(5)
            self.sch_3()
            
        else:            
            if self._start_at == 0 and self._stimuli is None:
                # drive(stim_rx_2).after_every(stim_rx_1).start_at(0)
                self.sch_9()
                
            elif self._start_at > 0 and self._stimuli is None:
                # drive(stim_rx_2).after_every(stim_rx_1).start_at(3)
                self.sch_2()

            elif self._stimuli > 0:                 
                if self._start_at == 0:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0)
                    self.sch_5()
                        
                elif self._start_at > 0:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)
                    self.sch_6()
                                
                else:
                    # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3)
                    self.sch_4()
                    
            elif self._samples is None and self._samples_after is not None:
                # drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9])
                self.sch_7()
                
            elif self._samples is not None and self._samples_after is not None:
                # drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9])
                self.sch_8()
                
            else:
                # drive(stim_rx_2).after_every(stim_rx_1)                
                self.sch_1()    
                

    # TODO: Check the shorter list and limit the generation
    def sch_1(self): # drive(stim_rx_2).after_every(stim_rx_1) t2
        for i in range(len(self._stimuli_list)):
            self.cond_list.append( (i, (self._name_after, i) ) )

    def sch_2(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(3) t3
        for i in range(len(self._stimuli_list)):
            sample = (self._start_at - 1) + i
            self.cond_list.append( (i, (self._name_after, sample ) ) )
            if sample >= len(self._after_every) - 1:
                return
            
    def sch_3(self): # drive(stim_rx_2).after(stim_rx_1).start_at(5) t4 
        self.cond_list.append( (0, (self._name_after, self._start_at-1) ) )
        
    def sch_4(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3) t5
        for i in range(len(self._stimuli_list)):
            sample = (self._stimuli - 1) + (i * self._stimuli)
            self.cond_list.append( (i, (self._name_after, sample) ) )
            if sample >= len(self._after_every) - self._stimuli:
                return
            
    def sch_5(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0) t6
        for i in range(len(self._stimuli_list)):
            src_sample = i + 1
            sample = (self._stimuli - 1) + (i * self._stimuli)
            self.cond_list.append( (src_sample, (self._name_after, sample) ) )
            if sample >= len(self._after_every) - self._stimuli:
                return
            
    def sch_6(self): # drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3) t7
        for i in range(len(self._stimuli_list)):
            sample = (self._start_at - 1) + (i * self._stimuli)    
            self.cond_list.append( (i, (self._name_after, sample) ) )
            if sample >= len(self._after_every) - self._stimuli:
                return
            
    def sch_7(self): # drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9]) t8
        for i, s in enumerate(self._samples_after):
            self.cond_list.append( (i, (self._name_after, s-1) ) )
            
    def sch_8(self): # drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9]) t9
        for i, s in zip(self._samples, self._samples_after):
            self.cond_list.append( (i-1, (self._name_after, s-1) ) )
            
    def sch_9(self): # drive(stim_rx_2).after_every(stim_rx_1).start_at(0) t10
        for i in range(1, len(self._stimuli_list)):
            self.cond_list.append( (i, (self._name_after, i-1) ) )
            
            
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

def get( name ):
    for config in default_scheduler.configs:
        if name == config._name:
            return config.get()
    return []

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


# Some usage examples
if __name__ == '__main__':
    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]
    
    print_configurations() # Nothing to print
    
#    drive(stim_rx_2).after_every(stim_rx_1).after(stim_rx_1) # Detect ERROR
#    drive(stim_rx_2).after(stim_rx_1).start_at(5).after_every(stim_rx_1) # Detect ERROR
    drive(stim_rx_2).after_every(stim_rx_1)                                     # test_002
    drive(stim_rx_2).after_every(stim_rx_1).start_at(3)                         # test_003
    drive(stim_rx_2).after(stim_rx_1).start_at(5)                               # test_004 (Enable after 5)
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3)                          # test_005
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0)              # test_006 (1st sample after reset)
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)              # test_007
    drive(stim_rx_2).after(stim_rx_1).samples([3, 7, 8])                        # test_008 (1 after 3, 2 after 7, 3 after 8)
    drive(stim_rx_2).samples([2, 4, 7]).after(stim_rx_1).samples([1, 4, 8])     # test_009 (2 after 1, 4 after 4, 7 after 8)

    drive(stim_rx_2).with_gaps(4)
    
    # Pink-Ponk
    drive(stim_rx_2).after_every(stim_rx_1).start_at(0) # start_at(0) == drive first sample after reset w/o condition
    drive(stim_rx_1).after_every(stim_rx_2)
    # ---------
    
    print_configurations()
    
    print_schedules()    
    
    clear_configurations()
    print_configurations()
