from myhdl import *

class Schedulable():
    '''|
    | This class executes schedules of driving stimuli and capture outputs during testing
    |________'''
    def __init__(self):
        self.cntr_map = {}

    def count(self, cnt, done, end, N):
        '''|
        | Counts events (data items sent or received). Signals END when a predefined number N is reached
        |________'''
        @instance
        def count_inst():
            end.next = False
            while True:
                if cnt.next == N:
                    end.next = True
                yield done
                cnt.next += 1

        return count_inst


    def evaluate(self, tpls):
        '''|
        | Evaluates a single condition or a list of conditions (ANDed). Yields when the condition evaluates as True.
        | Condition is a tuple: (port_name, data_item_index)
        |     port_name - string, name of a port
        |     data_item_index - int, index of a data item send/received on the port given by port_name
        | A condition evaluates True when the data item port_name[data_item_index] has been sent/received
        |________'''
        if not isinstance(tpls, list):
            tpls = [tpls]

        for name, index in tpls:
            cnt = self.cntr_map[name]
            while not cnt >= index + 1:
                yield cnt


    def en_interface(self, clk, start, ipg, cnt, en, cond_lst):
        '''|
        | Generates drive/capture enable signals based on evaluation of the conditions and inter-packet gap
        |________'''
        @instance
        def enbl():
            yield start

            # default schedule with IPG in case of empty condition list
            if len(cond_lst) == 0:
                i = 0
                while True:
                    while not (cnt >= i):
                        yield cnt

                    # Inter-Packet Gap
                    for _ in range(ipg):
                        yield clk.posedge

                    en.next = not en
                    i += 1
            #--------------------------------------------------
            i = 0
            condition = cond_lst.pop(0)
            while True:
                while not (cnt == i):
                    yield cnt

                ipg_loc = ipg

                if condition[0] == i:
                    yield self.evaluate(condition[1])

                    # Get optional local ipg
                    if len(condition) > 2:
                        ipg_loc = condition[2]

                    if len(cond_lst):
                        condition = cond_lst.pop(0)

                # Inter-Packet Gap
                for _ in range(ipg_loc):
                    yield clk.posedge

                en.next = not en
                i += 1

        return enbl


    def gen(self, rst, clk, shed_param, tst_data, sim_time):
        '''|
        | Generates all the instances needed to implement a scheduler
        | ls_x - list of port parameters, one parameter per port.
        | A parameter is a tuple (port_name, done_signal, enable_signal, ipg)
        |________'''
        ls_counters = []
        ls_checkers = []

        ls_sim_end = []
        cond_sim_end = tst_data["cond_sim_end"]

        start = Signal(bool(0))
        sim_end = Signal(bool(0))

        for name, (done, en, ipg) in shed_param.iteritems():
            cntr = Signal(int(0))
            end = Signal(bool(0))
            ls_sim_end.append(end)

            self.cntr_map[name] = cntr
            ls_counters.append(self.count(cntr, done, end, cond_sim_end[name]))
            ls_checkers.append(self.en_interface(clk, start, ipg, cntr, en, tst_data["cond_" + name]))

        sim_ctrl = self.simulation_control(rst, clk, start, sim_time, sim_end)

        @always_comb
        def sim_done():
            x = True
            for s in ls_sim_end:
                x = x and s
            sim_end.next = x

        return instances()


    def simulation_control(self, rst, clk, en_ctrl, sim_time, sim_end):
        '''|
        | Used to control the simulation:
        |     1) enable the drivers and the scheduler after reset
        |     2) stop the simulation after predefined time or after the scheduler indicates
        |________'''

        @instance
        def simControl():
            yield clk.posedge # rst needs 1 clk to get its value

            if rst.active:
                while rst:
                    yield clk.posedge
            else:
                while not rst:
                    yield clk.posedge

            en_ctrl.next = True

            if sim_time == "auto":
                yield sim_end

                for i in range(10):
                    yield clk.posedge
            else:
                for i in range(sim_time):
                    yield clk.posedge

            # End of simulation
            raise StopSimulation

        return instances()