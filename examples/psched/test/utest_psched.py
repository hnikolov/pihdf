import unittest

from pihdf import pschedule

from myhdl_lib import *

from t_psched import t_psched

# TODO -----------------------------------------------------
def stream_gen_list(dimensions=None, sequential=True, max_num={'pkts':3, 'bytes': 150}):
    """ Returns a random generated stream; stream=list_of_packets; packet=list_of_bytes; byte = int(rand(), min=0, max=255)
        Parameters:
            dimensions - defines the sizes of the stream, the packets and the messages, e.g.:
                None               - a random generated stream
                5                  - stream of 5 packets
                [3]                - stream of one packet containing 3 bytes
                [2,4,6]            - stream of 3 packets containing respectively 2, 4, and 6 bytes
            max_num - defines the maximum of the ranges for the unspecified dimensions, e.g:
                'byts':10 - means that the unspecified message length will be chosen randomly in the range 1..10 bytes per message
                'msgs':3  - means that the unspecified packet length will be chosen randomly in the range 1..3 messages per packet
                'pkts':3  - means that the unspecified stream length will be chosen randomly in the range 1..3 packets per stream
            sequential - defines how the message bytes are generated; when sequential=True, the bytes are number sequence, otherwise they are random integers in the range 0..2555 
    """
    dim = dimensions
    # What "dim" is? None, int, list, rubbish?
    while True:
        if (not dim):
            dim = random.randint(1,max_num['pkts'])                 
        if (isinstance(dim,int)):
            dim = [random.randint(1,max_num['bytes']) for p in range(dim)]       
        if (isinstance(dim,list)): 
            break
        else:
            dim = None
            
#    print "dim=", dim

    def next_i():
        next_i.i = (next_i.i+1)%0x100
        return next_i.i       
    next_i.i = 0;
    stream = []
    if (sequential) :
        stream = [[next_i() for b in range(p)] for p in dim]
    else :
        stream = [[random.randint(0,0xFF) for b in range(p)] for p in dim]           
#    print "stream_in=", stream
    return stream

        

#---------------------------
def stream_gen_string(dimensions=None, sequential=True):
    stream_str = []
    for pkt in stream_gen_list(dimensions, sequential):
        stream_str.append(str(bytearray(pkt)))
    return stream_str
#-------------------------------------------------------------



class Test_psched(t_psched):
    '''|
    | The main class for unit-testing. Add your tests here.
    |________'''
    def __init__(self):
        # call base class constructor
        t_psched.__init__(self)

    # Automatically executed BEFORE every TestCase
    def setUp(self):
        t_psched.setUp(self)

    # Automatically executed AFTER every TestCase
    def tearDown(self):
        t_psched.tearDown(self)


    # generate stimuli and reference data:
    def use_data_set_1(self):
        l = range(26,36)
        payload = stream_gen_string(l)

        for i in range(len(l)):
            fields_in = { 'cmd': 0, 'port': (3000+i) }
            self.stim_rx_port.append( fields_in )
            self.ref_tx_port.append( fields_in )

        for i in payload:
            self.stim_rx.append({"payload":i})
            self.ref_tx.append({"payload":i})
        

    def use_data_set_2(self):
        payload = stream_gen_string(3*3*[80])

        for i in range(3):
            fields_in = { 'cmd': 0, 'port': (3000+i) }
            self.stim_rx_port.append( fields_in )
            self.ref_tx_port.append( fields_in )

            for j in range(3):
                pld = payload.pop(0)
                self.stim_rx.append({"payload":pld})
                self.ref_tx.append({"payload":pld})
        
    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_000(self):
        """ >>>>>> TEST_000: Pass-through, using default schedule for rx_port and rx """
        self.models = {"top":self.BEH}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":False, "fdump":False}
        self.use_data_set_1()
        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_001(self):
        """ >>>>>> TEST_001: Pass-through, using default schedule for rx_port and rx """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False, "ipgi":1, "ipgo":1}
        self.use_data_set_1()
        self.run_it()

# --------------------------------------------------------------------------------
# Schedule input interfaces stimuli data
# --------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_002(self):
        """ >>>>>> TEST_002: Schedule every rx_port stimuli after every rx stimuli """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        '''
        self.cond_rx_port += [(0,("rx",0)),
                              (1,("rx",1)),
                              (2,("rx",2)),
                              (3,("rx",3)),
                              (4,("rx",4)),
                              (5,("rx",5)),
                              (6,("rx",6)),
                              (7,("rx",7)),
                              (8,("rx",8)),
                              (9,("rx",9))]
        '''                              

        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx)
#        pschedule.print_configurations()
#        pschedule.print_schedules()
        
        # Expected sequence
        for _ in range(10):
            self.ref_sequence.append({"data":2})
            self.ref_sequence.append({"data":1})

        
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_003(self):
        """ >>>>>> TEST_003: Schedule every rx_port stimuli after every rx stimuli, start at 3. The last 3 rx_port stimuli are driven w/o conditions """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        '''
        self.cond_rx_port += [(0,("rx",2)),
                              (1,("rx",3)),
                              (2,("rx",4)),
                              (3,("rx",5)),
                              (4,("rx",6)),
                              (5,("rx",7)),
                              (6,("rx",8)),
                              (7,("rx",9))]
        '''                      

        self.use_data_set_1()

        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx).start_at(3)

        # Expected sequence
        self.ref_sequence.append({"data":2})
        self.ref_sequence.append({"data":2})
        self.ref_sequence.append({"data":2})

        for _ in range(7):
            self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":2})

        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":1})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_004(self):
        """ >>>>>> TEST_004: Enable rx_port stimuli after 5th rx stimuli """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        #self.cond_rx_port += [(0,("rx",4))]
                              
        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).after(self.stim_rx).start_at(5)
        
        # Expected sequence
        for _ in range(5):
            self.ref_sequence.append({"data":2})

        for _ in range(2):
            for _ in range(3):
                self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":3})

        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":1})

        for _ in range(3):
            self.ref_sequence.append({"data":2})

        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_005(self):
        """ >>>>>> TEST_005: Schedule every rx_port stimuli after every 3 rx stimuli. The last X rx_port stimuli are driven w/o conditions """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        '''
        self.cond_rx_port += [(0,("rx",2)),
                              (1,("rx",5)),
                              (2,("rx",8))]
        '''

        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx).stimuli(3)

        # Expected sequence
        for _ in range(3):
            for _ in range(3):
                self.ref_sequence.append({"data":2})
            self.ref_sequence.append({"data":1})

        for _ in range(3):
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":3})
        
        for _ in range(3):
            self.ref_sequence.append({"data":1})
        
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_006(self):
        """ >>>>>> TEST_006: Schedule every rx_port stimuli after every 3 rx stimuli. 1st stimuli after reset. The last X rx_port stimuli are driven w/o conditions """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        '''        
        self.cond_rx_port += [(1,("rx",2)),
                              (2,("rx",5)),
                              (3,("rx",8))]
        '''                      

        self.use_data_set_1()

        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx).stimuli(3).start_at(0)
        
        # Expected sequence
        for _ in range(3):
            self.ref_sequence.append({"data":1})
            for _ in range(3):
                self.ref_sequence.append({"data":2})

        for _ in range(4):
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":3})
        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":1})

        
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_007(self):
        """ >>>>>> TEST_007: Schedule every rx_port stimuli after every 2 rx stimuli, starting after stimuli 3 of rx. The last X rx_port stimuli are driven w/o conditions """
        self.models = {"top":self.RTL}
        # Set fdump to True in order to generate test vector files for the global interfaces
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset
        '''        
        self.cond_rx_port += [(0,("rx",2)),
                              (1,("rx",4)),
                              (2,("rx",6)),
                              (3,("rx",8))]
        '''                      

        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx).stimuli(2).start_at(3)
        
        # Expected sequence
        for _ in range(3):
            self.ref_sequence.append({"data":2})


        for _ in range(3):
            self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":2})
            self.ref_sequence.append({"data":2})

        for _ in range(4):
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":3})
        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":1})
        
        self.run_it()

    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_008(self):
        """ >>>>>> TEST_008: Schedule rx stimuli 1, 2, and 3 after rx_port stimuli 4 and 8, and 9 """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}
               
        # Specify only iterations in which check has to be done
        '''       
        self.cond_rx_port += [(0,("rx",3)),
                              (1,("rx",7)),
                              (2,("rx",8))]
        '''                      
                                                            
        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).after(self.stim_rx).samples([4, 8, 9])
        
        # Expected sequence
        for _ in range(2):
            for _ in range(4):
                self.ref_sequence.append({"data":2})
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":2})

        for _ in range(4):
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":3})

        for _ in range(3):
            self.ref_sequence.append({"data":1})
        
        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_009(self):
        """ >>>>>> TEST_009: Schedule rx stimuli 3, 5, and 8 after rx_port stimuli 2, 5, and 9 """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}
               
        # Specify only iterations in which check has to be done
        '''        
        self.cond_rx_port += [(2,("rx",1)),
                              (4,("rx",4)),
                              (7,("rx",8))]
        '''                      
                                                            
        self.use_data_set_1()
        
        pschedule.drive(self.stim_rx_port).samples([3, 5, 8]).after(self.stim_rx).samples([2, 5, 9])

        # Expected sequence
        for _ in range(2):
            self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":2})
            self.ref_sequence.append({"data":2})

        self.ref_sequence.append({"data":2})

        for _ in range(3):
            self.ref_sequence.append({"data":1})

        for _ in range(4):
            self.ref_sequence.append({"data":2})

        for _ in range(3):
            self.ref_sequence.append({"data":1})

        self.ref_sequence.append({"data":2})
        
        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_010(self):
        """ >>>>>> TEST_010: Pink-Ponk - Schedule every rx stimuli after rx_port stimuli; and every rx_port stimuli after rx stimuli. The first rx_prot stimuli start after reset """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        # NOTE: If rx_port[0] not in the list, then rx_port is driven immediately after reset

        #              iteration(== #packet-1),[Conditions == "interface", #packet]
        '''        
        self.cond_rx_port += [(1,("rx",0)),
                              (2,("rx",1)),
                              (3,("rx",2)),
                              (4,("rx",3)),
                              (5,("rx",4)),
                              (6,("rx",5)),
                              (7,("rx",6)),
                              (8,("rx",7)),
                              (9,("rx",8))]

        self.cond_rx += [(0,("rx_port",0)),
                         (1,("rx_port",1)),
                         (2,("rx_port",2)),
                         (3,("rx_port",3)),
                         (4,("rx_port",4)),
                         (5,("rx_port",5)),
                         (6,("rx_port",6)),
                         (7,("rx_port",7)),
                         (8,("rx_port",8)),
                         (9,("rx_port",9))]
        '''
        self.use_data_set_1()

        pschedule.drive(self.stim_rx_port).after_every(self.stim_rx).start_at(0)
        pschedule.drive(self.stim_rx).after_every(self.stim_rx_port)

        # Expected sequence
        for _ in range(10):
            self.ref_sequence.append({"data":1})
            self.ref_sequence.append({"data":2})

        self.run_it()


    # ----------------------------------------------------------------------------
    # @unittest.skip("")
    def test_011(self):
        """ >>>>>> TEST_011: Schedule - rx_port stimuli 2 after rx stimuli 2, rx_port stimuli 3 after rx stimuli 6; rx stimuli 3 after rx_port stimuli 2, rx stimuli 7 after rx_port stimuli 3 """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}
               
        # Specify only iterations in which check has to be done
        '''
        self.cond_rx_port += [(1,("rx",1)),
                              (2,("rx",5))]
                              
        #              iteration,[Conditions] (Considered True for omitted iterations)
        self.cond_rx      += [(2,("rx_port",1)),
                              (6,("rx_port",2))]
        '''
        self.use_data_set_2()

        pschedule.drive(self.stim_rx_port).samples([2, 3]).after(self.stim_rx).samples([2, 6])
        pschedule.drive(self.stim_rx).samples([3, 7]).after(self.stim_rx_port).samples([2, 3])

        # Expected sequence
        self.ref_sequence.append({"data":1})
        self.ref_sequence.append({"data":2})
        self.ref_sequence.append({"data":2})
        self.ref_sequence.append({"data":1})
        
        for _ in range(4):
            self.ref_sequence.append({"data":2})

        self.ref_sequence.append({"data":1})
        
        for _ in range(3):
            self.ref_sequence.append({"data":2})

        self.run_it()

# --------------------------------------------------------------------------------
# Schedule capturing output interfaces
# --------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_023(self):
        """ >>>>>> TEST_023: Start capturing tx_port data after 4rd rx stimuli """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        self.use_data_set_1()

        pschedule.capture(self.res_tx_port).after(self.stim_rx).start_at(4)
#        pschedule.print_configurations()
#        pschedule.print_schedules()

        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_029(self):
        """ >>>>>> TEST_029: Capture tx results data 3, 5, and 8 after rx_port stimuli 2, 5, and 9 """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}

        self.use_data_set_1()

        pschedule.capture(self.res_tx_port).samples([3, 5, 8]).after(self.stim_rx).samples([2, 5, 9])

        self.run_it()

# -------
# TODOs
#--------

    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_106(self):
        """ >>>>>> TEST_106: Schedule - rx starts after rx_port stimuli (index) 6 (with 'ipg' clk cycles delay). There is inter-packet gap (ipgi) between the packets """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False, "ipgi":5}

        #              iteration(== #packet-1),[Conditions == "interface", #packet-1]
        self.cond_rx += [(0,("rx_port",6))]
        
#        pschedule.drive(self.stim_rx).after(self.stim_rx_port).with_gaps(5) # Enable rx after 6 samples of rx_port with ipg=5

        self.use_data_set_1()
        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_103(self):
        """ >>>>>> TEST_103: Schedule - rx_port stimuli (index) 1 after (tx_port AND tx packets) 0 (with 1 clk delay), and so on """
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False}
            
        # TODO: regular, could the specification of this schedule be simplified?
        #              iteration,[Conditions]
        self.cond_rx_port += [(1,[("tx_port",0),("tx",0)]),
                              (2,[("tx_port",1),("tx",1)]),
                              (3,[("tx_port",2),("tx",2)]),
                              (4,[("tx_port",3),("tx",3)]),
                              (5,[("tx_port",4),("tx",4)]),
                              (6,[("tx_port",5),("tx",5)]),
                              (7,[("tx_port",6),("tx",6)]),
                              (8,[("tx_port",7),("tx",7)]),
                              (9,[("tx_port",8),("tx",8)])]

#        pschedule.drive(self.stim_rx_port).after_every([self.res_tx_port, self.res_tx])
        
        self.use_data_set_1()
        self.run_it()


    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_107(self):
        """ >>>>>> TEST_107: Free running - NO inter-packet gaps """
        self.verbose = True
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":150, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}
        self.use_data_set_1()
        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_108(self):
        """ >>>>>> TEST_108: Free running - Inter-packet gaps = 0, Get overriden to IPG=1 """
        self.verbose = True
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":"auto", "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":0}
        self.use_data_set_1()
        self.run_it()

    # ----------------------------------------------------------------------------
    @unittest.skip("RTL needs parameters")
    def test_109(self):
        """ >>>>>> TEST_109: Inter-packet gaps at the output in order to push-back"""
        self.models = {"top":self.RTL}
        self.tb_config = {"simulation_time":150, "cosimulation":False, "trace":True, "fdump":False, "ipgi":0, "ipgo":4}
        self.use_data_set_1()
        self.run_it()

