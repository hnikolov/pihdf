import myhdl
from myhdl import *

class Reset(myhdl.ResetSignal):
    '''|
    | The reset signal type of pihdf
    | It inherits the myhdl Reset signal and keeps the reset's instance name
    |________'''
    def __init__(self, name=None, active=1, val=1, async=True):
        myhdl.ResetSignal.__init__(self, val, active, async)
        self.inst_name = name
        self.class_name = self.__class__.__name__

    """ Reset pulse (synchronous with the rising edge of the clk """
    def pulse(self, clk, RST_Length_cc=10):
        @instance
        def _reset():
            self.next = self.active
            for i in range(RST_Length_cc):
                yield clk.posedge
            self.next = not self.active
        return _reset


class Clock(myhdl.SignalType):
    '''|
    | The clock signal type of pihdf
    | It inherits myhdl SignalType and keeps the clk's instance name
    |________'''
    def __init__(self, name=None, val=1):
        myhdl.SignalType.__init__(self, val=bool(val))
        self.inst_name = name
        self.class_name = self.__class__.__name__

    """ Clock generator """
    def gen(self, CLK_Period_ns=1): # default period (1 == 20ns)
        @instance
        def _clock():
            self.next = False
            while True:
                yield delay(CLK_Period_ns)
                self.next = not self.val
        return _clock


class Parameter(object):
    '''|
    | The parameter type of pihdf. It has a name and a value
    |________'''
    def __init__(self, name=None, value=None):
        self.inst_name = name
        self.value = value
        self.class_name = self.__class__.__name__

    def __str__(self):
        return self.inst_name
