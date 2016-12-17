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

    def clear(self):
        self.configs = []
        
    def print_configurations(self):
        """
        Prints the configurations of all stimuli
        """
        if self.configs == []:
            print "Nothing to print"

        for config in self.configs:
            config.print_configuration()


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

    def find_name_after(self, sname, lo):
        (filename,line_number,function_name,text)=traceback.extract_stack()[lo]
        idx = text.find(sname)

        if idx != -1:
            text = text[idx:]
            return text[len(sname):text.find(')')].strip()
            
        return "NO NAME FOUND"         

    def after_every(self, stimuli):
        if self._after is not None:
            print 'In "after_every": Use either "after_every" or "after"'
            exit()
            
        self._after_every = stimuli
        self._name_after = self.find_name_after('every(', lo=-3)
        return self

    def after(self, stimuli):
        if self._after_every is not None:
            print 'In "after": Use either "after_every" or "after"'
            exit()

        self._after = stimuli
        self._name_after = self.find_name_after('after(', lo=-3)
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

    def get_cond_list(self):
        pass
        
# The following methods are shortcuts for not having to
# create a Scheduler instance:

#: Default :class:`Scheduler <Scheduler>` object
default_scheduler = Scheduler()


def drive( stimuli ): # TODO: Should be the same for 'drive' and 'capture'
    """
    ... with the default module scheduler.

    :return: The default :obj:`Scheduler` instance
    """
    return default_scheduler.add( stimuli )

def clear_configurations():
    default_scheduler.clear()
    
def print_configurations():
    default_scheduler.print_configurations()


if __name__ == '__main__':
    stim_rx_1 = [1, 3, 5, 7,  9]
    stim_rx_2 = [2, 4, 6, 8, 10]
    
    print_configurations() # Nothing to print
    
#    drive(stim_rx_2).after_every(stim_rx_1).after(stim_rx_1) # Detect ERROR
#    drive(stim_rx_2).after(stim_rx_1).start_at(5).after_every(stim_rx_1) # Detect ERROR
    drive(stim_rx_2).after_every(stim_rx_1)
    drive(stim_rx_2).after_every(stim_rx_1).start_at(3)
    drive(stim_rx_2).after(stim_rx_1).start_at(5) # Enable after 5
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3)
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(3).start_at(0) # 1st sample after reset
    drive(stim_rx_2).after_every(stim_rx_1).stimuli(2).start_at(3)
    drive(stim_rx_2).after(stim_rx_1).samples([4, 8, 9]) # 1 after 4, 2 after 8, 3 after 9
    drive(stim_rx_2).samples([3, 5, 8]).after(stim_rx_1).samples([2, 5, 9]) # 3 after 2, 5 after 5, 8 after 9

    drive(stim_rx_2).with_gaps(4)
    
    # Pink-Ponk
    drive(stim_rx_2).after_every(stim_rx_1).start_at(0) # start_at(0) == drive first sample after reset w/o condition
    drive(stim_rx_1).after_every(stim_rx_2)
    # ---------
    
    print_configurations()
    clear_configurations()
    print_configurations()
    
