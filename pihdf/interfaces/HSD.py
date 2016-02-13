from myhdl import *
from pihdf import mylog
from myhdl_lib import fifo, arbiter

from collections import OrderedDict

import traceback
import os, sys


class HSD(object):
    '''|
    | A generic hand-shake interface used for (safe) communication between HW modules.
    | The interface has source and sink sides. Each side has ready, valid, and data signals to implement a push-back behavior.
    | The source side is used to write data to the interface: when ready is active, drive data and valid.
    | The sink side is used to consume data from the interface: consume data when it is valid, drive ready accordingly.
    | Data width is configurable via a constructor argument.
    | The interface may contain a FIFO buffer connecting the source and sink sides. The FIFO depth is configurable via method 'gen()'
    | The interface supports also a push behavior, i.e., the data from the source side is propagated to the sink side assuming that
    | the consumer of the data is always ready. Useful when implementing control interfaces.
    |________'''
    def __init__(self, data=None, name=None, direction=None, buf_size=0, push=False, terminate=False, filedump=None, lo=-2):

        if name == None:
            (filename,line_number,function_name,text)=traceback.extract_stack()[lo]
            self.inst_name = text[text.find('.')+1:text.find('=')].strip()  # skip 'self.'
            if self.inst_name=='':
                self.inst_name = text[:text.find('=')].strip()
        else:
            self.inst_name = name

        if direction != None:
            self.direction = direction # IN (SNK) or OUT (SRC)

        self.class_name = self.__class__.__name__

        self.buf_size = buf_size
        self.push = push
        self.terminate = terminate
        self.filedump = False
        
        if filedump != None:
            self.filename = filedump + self.inst_name + ".tvr" # to dump test vectors
            # deletes the content of the file if present
            with open(self.filename, "wb") as f:
                self.filedump = True

        ready_default_value = push or terminate

        self.src_ready  = Signal(bool(ready_default_value))
        self.src_valid  = Signal(bool(0))

        if buf_size > 0:
            self.snk_ready  = Signal(bool(ready_default_value))
            self.snk_valid  = Signal(bool(0))
        else:
            self.snk_ready  = self.src_ready
            self.snk_valid  = self.src_valid

        if data != None:
            if isinstance(data, int):
                if data > 1:
                    self.data = [("data", intbv(0)[data:])]
                elif(data == 1):
                    self.data = [("data", bool(0))]
                else:
                    assert "HSD: Non-positive data width: {}".format(data)
            else:
                self.data = data

            self._src_signals = []
            self._snk_signals = []
            self._sig_names   = []
            self._sig_lens    = []

            for f_name, f_type in self.data:
                src_sig = Signal(f_type)
                snk_sig = Signal(f_type)

                self._src_signals.append( src_sig )

                if buf_size > 0:
                    self._snk_signals.append( snk_sig )

                self._sig_names.append(f_name)
                self._sig_lens.append(len(src_sig))

            if buf_size == 0:
                self._snk_signals = self._src_signals

            self.srcDataList = [] # for DRIVING signals
            self.snkDataList = [] # for READING signals

    @staticmethod
    def _assign_signal(aIn, aOut):
        """ Helper function, generates a combinatorial signal assignment """
        @always_comb
        def asgn():
            aOut.next = aIn
        return asgn

    #========================================================================
    def gen(self, rst=None, clk=None):
        '''|
        | Implementation of the interface, FIFO is instantiated between the src and snk data
        |________'''
        assert( not(self.push and self.buf_size > 0) ), \
        "Interface '{:}' ({:}) of type 'push' can not use a fifo buffer! Currently set to size {:}.".\
        format(self.inst_name, self.class_name, self.buf_size)

        #assert( not(not(hasattr(self, 'data')) and self.buf_size > 0) ), \
        #"Interface '{:}' ({:}) with no data can not use a fifo buffer! Currently set to size {:}.".\
        #format(self.inst_name, self.class_name, self.buf_size)

        if self.buf_size > 0 and not self.push:
            #--------------------
            # Handshake with fifo
            #--------------------
            src_ready = self.src_ready
            src_valid = self.src_valid
            src_data = ConcatSignal(*self._src_signals) if len(self._src_signals) > 1 else self._src_signals[0]

            snk_ready = self.snk_ready
            snk_valid = self.snk_valid
            snk_data = Signal(intbv(0)[len(src_data):])

            sig_full, sig_mty = [Signal(bool(0)) for i in range(2)]

            @always_comb
            def assign():
                src_ready.next = not sig_full
                snk_valid.next = not sig_mty

            inst_fifo = fifo( rst   = rst
                            , clk   = clk
                            , we    = src_valid
                            , din   = src_data
                            , full  = sig_full
                            , re    = snk_ready
                            , dout  = snk_data
                            , empty = sig_mty
                            , depth = self.buf_size)

            widths = self._sig_lens
            hi = [sum(widths[i:]) for i in range(len(widths))]
            lo = [hi[i]-widths[i] for i in range(len(widths))]
            slices = [(snk_data(hi[i],lo[i]) if (widths[i] != 1) else snk_data(lo[i])) for i in range(len(widths))]

            x = []
            for i, slc in enumerate(slices):
                x.append(self._assign_signal(slc, self._snk_signals[i]))

        # Always perform the call to instances() - seems to preserve the hierarchy
        return instances()


    #========================================================================
    def get_src_signals(self):
        '''|
        | Returns the source signals
        |________'''
        return [self.src_ready, self.src_valid] + self._src_signals


    def get_snk_signals(self):
        '''|
        | Returns the sink signals
        |________'''
        return [self.snk_ready, self.snk_valid] + self._snk_signals


    def get_sig_names(self):
        '''|
        | Returns the signals' names
        |________'''
        return ['ready', 'valid'] + self._sig_names


    def get_sig_full_names(self):
        '''|
        | Returns the signals' names prepended with the instance name
        |________'''
        return [self.inst_name + "_" + name for name in self.get_sig_names()]


    def get_sig_lens(self):
        '''|
        | Returns the signals' lens
        |________'''
        return [1, 1] + self._sig_lens


    def get_all_signals(self):
        '''|
        | Returns OrderedDictionaly of all interface snk or src signals, depending on the interface direction
        |________'''
        names = self.get_sig_full_names()
        signals = []
        if self.direction==0:  # IN
            signals = (self.get_snk_signals())
        elif self.direction==1:  # OUT
            signals = (self.get_src_signals())
        else:
            raise ValueError, "Unknown direction %d".format(self.direction)

        return OrderedDict(zip(names, signals))

    #========================================================================
    def assign(self, ready, valid, *args):
        '''|
        | Assigns all interface signals on a side snk/src depending on the interface direction
        |________'''
        if self.direction==0:  # IN
            return self.assignRX(ready, valid, *args)
        elif self.direction==1:  # OUT
            return self.assignTX(ready, valid, *args)
        else:
            raise ValueError, "Unknown direction %d".format(self.direction)


    def assignRX(self, rx_ready, rx_valid, *args):
        """|
        | Connect interface signals. Used in function Convert()
        |________"""
        snk_ready = self.snk_ready
        snk_valid = self.snk_valid
        snk_data  = self._snk_signals

        @always_comb
        def assign_rx():
            snk_valid.next = rx_valid
            rx_ready.next  = snk_ready

        x = []
        for i, s in enumerate(args):
            x.append(self._assign_signal(s, snk_data[i]))

        return instances()


    def assignTX(self, tx_ready, tx_valid, *args):
        '''|
        | Connect interface signals. Used in function Convert()
        |________'''
        src_ready = self.src_ready
        src_valid = self.src_valid
        src_data  = self._src_signals

        @always_comb
        def assign_tx():
            src_ready.next = tx_ready
            tx_valid.next  = src_valid

        x = []
        for i, s in enumerate(args):
            x.append(self._assign_signal(src_data[i], s))

        return instances()


    #========================================================================
    def fdump(self, filename=""):
        '''|
        | Set file dump
        |________'''
        self.filename = filename

        # deletes the content of the file if present
        with open(self.filename, "wb") as f:
            self.filedump = True


    def getStimuli(self, inData):
        '''|
        | Get stimuli data from file
        |________'''
        stim_data_rx = []
        pld = {}
        x = self._sig_names
        try:
            with open(inData[0]["file"], 'rb') as myfile:
                for line in myfile.readlines():
                    for name,pckt in zip(x, line.split()):
                        pld[name] = int(pckt)
                    stim_data_rx.append(pld)
                    pld = {}
        except IOError:
            mylog.err("Stimuli file not found for " + self.inst_name + ":" + inData[0]["file"])

        return stim_data_rx

    #========================================================================
    def append(self, val, use_dict=False):
        '''|
        | Add a stimuli packet to the source data list
        |________'''
        if use_dict:
            y = []
            for name in self._sig_names:
                y.append(val[name])
            self.srcDataList.append( (y) )
        else:
            if len(self._sig_names) > 1:
                self.srcDataList.append( (val) )
            else:
                self.srcDataList.append( ([val]) )

    def get(self, use_dict=False):
        '''|
        | Returns a packet from the sink data list
        | Before calling, first check the list with hasPacket()
        | If filedump is set, this function also stores the data to file
        |________'''
        fdata_list = ''
        while len(self.snkDataList):
            pkt_tpl = self.snkDataList.pop(0)

            fdata_list = ' '.join(str(i) for i in pkt_tpl)
            if self.filedump:
                with open(self.filename, "a") as f:
                    f.write(fdata_list + '\n')

            if use_dict:
                y = {}
                for i, name in enumerate(self._sig_names):
                    y[name] = pkt_tpl[i]

                return y
            else:
                return list(pkt_tpl) if len(pkt_tpl) > 1 else pkt_tpl[0]


    def hasPacket(self):
        '''|
        | Returns true if the sink data list contains a packet
        | In order to provide correct behavior, this function
        | can be overridden by child interface classes
        |________'''
        return len(self.snkDataList) > 0


    #========================================================================
    def driver(self, clk, enable, done, tst_data):
        '''|
        | Instantiates a proper interface driver depending on the interface direction
        |________'''
        if self.direction==0:  # IN
            return self.driveInput(clk, enable, done, tst_data["stim_"+self.inst_name])
        elif self.direction==1:  # OUT
            return self.captureOutput(clk, enable, done, tst_data["res_"+self.inst_name])
        else:
            raise ValueError, "Unknown direction %d".format(self.direction)


    def driveInput(self, clk, enable, done, tst_data):
        '''|
        | Drive input. Used in function simulationControl()
        |________'''
        stim_data_rx = self.getStimuli(tst_data) if tst_data and "file" in tst_data[0] else tst_data

        '''|
        | Drives data from source data list to the interface signals. Not for synthesis
        |________'''
        @instance
        def rxLogic():
            yield enable

            while True:
                '''|
                | The link between unit test and low-level interface timing (fromList)
                |________'''
                if len(stim_data_rx) > 0:
                    self.append(stim_data_rx.pop(0), use_dict=True)
                else:
                    return

                yield self.fromList(clk)

                done.next = not done
                yield enable

        return instances()


    def fromList(self, clk):
        '''|
        | Drives data from source data list to the interface signals. Not for synthesis
        |________'''
        while not len(self.srcDataList): # needed in free-running mode
            yield clk.posedge

        while len(self.srcDataList):
            self.src_valid.next = 1

            src_sigs = self._src_signals
            tpl = self.srcDataList.pop(0)

            for i,val in enumerate(tpl):
                src_sigs[i].next = val

            yield clk.posedge

            # wait the data to be consumed
            while not self.src_ready:
                yield clk.posedge

        # Clear the value of the signals
        self.src_valid.next = 0
        for i,val in enumerate(src_sigs):
            src_sigs[i].next = 0


    def fromListInst(self, clk):
        @instance
        def _x():
            while True:
                yield self.fromList(clk)
        return _x


    def captureOutput(self, clk, enable, done, tst_data):
        '''|
        | Capture output. Used in function simulationControl()
        |________'''
        # Needed when fdump=False and dumping intermediate results (my_xxx.tvr), compare data using files
        if tst_data and "file" in tst_data[0]:
            self.fdump(tst_data[0]["file"])

        '''|
        | Capture data from the interface signals to the sink data list. Not for synthesis
        |________'''
        @instance
        def txLogic():
            yield enable

            while True:
                '''|
                | The link between low-level interface timing (toList) and unittest
                |________'''
                if self.hasPacket(): # hasPacket can be overwritten, e.g. STAvln
                    if tst_data and "file" in tst_data[0]:
                        self.get() # and dump it to file
                    else:
                        tst_data.append(self.get(use_dict=True))

                    done.next = not done
                    yield enable

                yield self.toList(clk)

        return instances()


    def toList(self, clk):
        '''|
        | Capture data from the interface signals to the sink data list. Not for synthesis
        |________'''
        self.snk_ready.next = 1

        yield clk.posedge
        while not self.snk_valid:
            yield clk.posedge

        self.snk_ready.next = 0 # needed when schedule is used

        snk_sigs = self._snk_signals
        l = [int(s) for s in snk_sigs]
        tpl = tuple(l)
        self.snkDataList.append( tpl )


    def toListInst(self, clk):
        @instance
        def _y():
            while True:
                yield self.toList(clk)
        return _y


    #========================================================================
    def enable(self, rst, clk, tx_ready, tx_valid, enable):
        '''|
        | Enable unit: Respects the handshake protocol. Data processing can be performed when enable is '1'
        |        tx_ready, tx_valid   - handshake of the output interface
        |        enable               - output, indicating that the input data (e.g., self.data) is valid and result has to be written to interface 'tx'
        |
        |        self.snk_ready, self.snk_valid   - handshake of this interface used as an input
        |________'''
        state = Signal(bool(0))

        @always_comb
        def rdy():
            self.snk_ready.next = 0
            enable.next   = 0

            if state == 0 or tx_ready:
                self.snk_ready.next = 1
                enable.next   = self.snk_valid

        @always_seq(clk.posedge, reset=rst)
        def clk_prcs():
            if self.snk_ready:
                state.next    = self.snk_valid
                tx_valid.next = self.snk_valid

        return instances()

    """
    The following code provides extra handshake functionality to be experimented with.
    We should decide whether the code should stay here.
    """

    @staticmethod
    def hs_join(ls_hsi, hso):
        """ (Many-to-one) Synchronizes multiple input handshake interfaces: output is ready when all inputs are ready
            ls_hsi - list of input (ready, valid) tuples
            hso    - a output (ready, valid) tuple
        """
        N = len(ls_hsi)
        ls_hsi_rdy, ls_hsi_vld = zip(*ls_hsi)
        ls_hsi_rdy, ls_hsi_vld = list(ls_hsi_rdy), list(ls_hsi_vld)
        hso_rdy, hso_vld = hso

        @always_comb
        def join_comb():
            all_vld = bool(1)
            for i in range(N):
                all_vld = all_vld and ls_hsi_vld[i]
            hso_vld.next = all_vld
            for i in range(N):
                ls_hsi_rdy[i].next = all_vld and hso_rdy

        return join_comb


    @staticmethod
    def hs_fork(hsi, ls_hso):
        """ (One-to-many) Broadcasts to multiple output handshake interfaces: input is ready when all outputs are ready
            hsi    - a input (ready, valid) tuple
            ls_hso - list of output (ready, valid) tuples
        """
        N = len(ls_hso)
        hsi_rdy, hsi_vld = hsi
        ls_hso_rdy, ls_hso_vld = zip(*ls_hso)
        ls_hso_rdy, ls_hso_vld = list(ls_hso_rdy), list(ls_hso_vld)

        @always_comb
        def fork_comb():
            all_rdy = bool(1)
            for i in range(N):
                all_rdy = all_rdy and ls_hso_rdy[i]
            hsi_rdy.next = all_rdy
            for i in range(N):
                ls_hso_vld[i].next = all_rdy and hsi_vld

        return fork_comb


    @staticmethod
    def hs_mux(sel, ls_hsi, hso):
        """ (Many-to-one) Multiplexes multiple input handshake interfaces
            ls_hsi - list of input (ready, valid) tuples
            hso    - a output (ready, valid) tuple
            sel    - selects an input handshake interface to be connected to the output
        """
        N = len(ls_hsi)
        ls_hsi_rdy, ls_hsi_vld = zip(*ls_hsi)
        ls_hsi_rdy, ls_hsi_vld = list(ls_hsi_rdy), list(ls_hsi_vld)
        hso_rdy, hso_vld = hso

        @always_comb
        def mux_comb():
            hso_vld.next = 0
            for i in range(N):
                ls_hsi_rdy[i].next = 0
                if i == sel:
                    hso_vld.next = ls_hsi_vld[i]
                    ls_hsi_rdy[i].next = hso_rdy

        return mux_comb


    @staticmethod
    def hs_demux(sel, hsi, ls_hso):
        """ (One-to-many) Demultiplexes to multiple output handshake interfaces
            hsi    - a input (ready, valid) tuple
            ls_hso - list of output (ready, valid) tuples
            sel    - selects an output handshake interface to connect to the input
        """
        N = len(ls_hso)
        hsi_rdy, hsi_vld = hsi
        ls_hso_rdy, ls_hso_vld = zip(*ls_hso)
        ls_hso_rdy, ls_hso_vld = list(ls_hso_rdy), list(ls_hso_vld)

        @always_comb
        def demux_comb():
            hsi_rdy.next = 0
            for i in range(N):
                ls_hso_vld[i].next = 0
                if i == sel:
                    hsi_rdy.next = ls_hso_rdy[i]
                    ls_hso_vld[i].next = hsi_vld

        return demux_comb


    @staticmethod
    def hs_arbmux(rst, clk, ls_hsi, hso, sel, ARBITER_TYPE="priority"):
        """ (Many-to-one) Arbitrates multiple input handshake interfaces
            Arbitrated only between inputs that currently have active valid
            ls_hsi - list of input (ready, valid) tuples
            hso    - a output (ready, valid) tuple
            sel    - output that indicates the currently selected input handshake interface
            ARBITER_TYPE - selects the type of arbiter to be used, priority or roundrobin
        """
        ls_vld = [hs[1] for hs in ls_hsi]
        sho_rdy, hso_vld = hso
        s = Signal(intbv(0), min=0, max=len(ls_vld))
        prio_update = Signal(bool(0))

        @always_comb
        def comb():
            prio_update.next = sho_rdy and hso_vld
            sel.next = s

        if (ARBITER_TYPE == "priority"):
            arb = arbiter.priority(ls_vld, s)
        elif (ARBITER_TYPE == "roundrobin"):
            arb = arbiter.roundrobin(rst, clk, ls_vld, s, prio_update)
        else:
            assert "hs_arbmux: Unknown arbiter type: {}".format(ARBITER_TYPE)

        mux = HSD.hs_mux(s, ls_hsi, hso)

        return instances()


    @staticmethod
    def hs_arbdemux(rst, clk, hsi, ls_hso, sel, ARBITER_TYPE="priority"):
        """(One-to-many) Arbitrates to multiple output handshake interfaces
            Arbitrates only between autputs that currently have active ready
            hsi    - a input (ready, valid) tuple
            ls_hso - list of output (ready, valid) tuples
            sel    - output that indicates the currently selected output handshake interface
            ARBITER_TYPE - selects the type of arbiter to be used, priority or roundrobin
        """
        shi_rdy, hsi_vld = hsi
        ls_rdy = [hs[0] for hs in ls_hso]
        s = Signal(intbv(0), min=0, max=len(ls_rdy))
        prio_update = Signal(bool(0))

        @always_comb
        def comb():
            prio_update.next = shi_rdy and hsi_vld
            sel.next = s

        if (ARBITER_TYPE == "priority"):
            arb = arbiter.priority(ls_rdy, s)
        elif (ARBITER_TYPE == "roundrobin"):
            arb = arbiter.roundrobin(rst, clk, ls_rdy, s, prio_update)
        else:
            assert "hs_arbdemux: Unknown arbiter type: {}".format(ARBITER_TYPE)

        demux = HSD.hs_demux(s, hsi, ls_hso)

        return instances()


    @staticmethod
    def data_mux(sel, ls_di, do):
        """ Multiplexes a list of input signals to a output signal """
        N = len(ls_di)
        @always_comb
        def mux_comb():
            do.next = 0
            for i in range(N):
                if i == sel:
                    do.next = ls_di[i]
        return mux_comb

    @staticmethod
    def data_demux(sel, di, ls_do):
        """ Demultiplexes an input signal to a list of output signals """
        N = len(ls_do)
        @always_comb
        def demux_comb():
            for i in range(N):
                ls_do.next = 0
                if i == sel:
                    ls_do.next = di
        return demux_comb

    @staticmethod
    def ls_data_mux(sel, lsls_di, ls_do):
        """ Multiplexes a list of input signal structures to an output structure. A structure is represented by a list of signals """
        N = len(ls_do)
        lsls_in = zip(*lsls_di)
        m = [HSD.data_mux(sel, lsls_in[i], ls_do[i]) for i in range(N)]
        return instances()

    @staticmethod
    def ls_data_demux(sel, ls_di, lsls_do):
        """ Demultiplexes an input signal structure to list of output structures. A structure is represented by a list of signals """
        N = len (ls_di)
        lsls_out = zip(*lsls_do)
        d = [HSD.data_demux(sel, ls_di[i], lsls_out[i])for i in range(N)]
        return instances()


    def join(self, ls_rx):
        """ Joins (synchronizes) a list of HSD instances to the self. The HSD data is not manipulated """
        ls_hs = [hs_if.get_snk_signals()[:2] for hs_if in ls_rx]
        hs_join = HSD.hs_join(ls_hs ,(self.src_ready, self.src_valid))
        return instances()


    def fork(self, ls_tx):
        """ Forks (broadcasts) self to a list of HSD instances. The HSD data is not manipulated """
        ls_hs = [hs_if.get_src_signals()[:2] for hs_if in ls_tx]
        hs_fork = HSD.hs_fork((self.snk_ready, self.snk_valid), ls_hs)
        return instances()


    def mux(self, sel, ls_rx, EXCLUDE_DATA=False):
        """ Multiplexes a list of HSD instances to self """
        ls_hs = [hs_if.get_snk_signals()[:2] for hs_if in ls_rx]
        hs_mux = HSD.hs_mux(sel, ls_hs ,(self.src_ready, self.src_valid))
        if not EXCLUDE_DATA:
            ls_data = [hs_if.get_snk_signals()[2:] for hs_if in ls_rx]
            data_mux = HSD.ls_data_mux(sel, ls_data, self.get_src_signals()[2:])
        return instances()


    def demux(self, sel, ls_tx, EXCLUDE_DATA=False):
        """ Demultiplexes self to a list of HSD instances """
        ls_hs = [hs_if.get_src_signals()[:2] for hs_if in ls_tx]
        hs_demux = HSD.hs_demux(sel, (self.snk_ready, self.snk_valid), ls_hs)
        if not EXCLUDE_DATA:
            ls_data = [hs_if.get_src_signals()[2:] for hs_if in ls_tx]
            data_demux = HSD.ls_data_demux(sel, self.get_snk_signals()[2:], ls_data)
        return instances()


    def arbmux(self, rst, clk, ls_rx, sel, ARBITER_TYPE="priority", EXCLUDE_DATA=False):
        """ Arbitrates a list of HSD instances to self """
        ls_hs = [hs_if.get_snk_signals()[:2] for hs_if in ls_rx]
        hs_arbmux = HSD.hs_arbmux(ls_hs, (self.src_ready, self.src_valid), sel, ARBITER_TYPE)
        if not EXCLUDE_DATA:
            ls_data = [hs_if.get_snk_signals()[2:] for hs_if in ls_rx]
            data_mux = HSD.ls_data_mux(sel, ls_data, self.get_src_signals()[2:])
        return instances()


    def arbdemux(self, rst, clk, ls_tx, sel, ARBITER_TYPE="priority", EXCLUDE_DATA=False):
        """ Arbitrates self to a list of HSD instances """
        ls_hs = [hs_if.get_src_signals()[:2] for hs_if in ls_tx]
        hs_arbdemux = HSD.hs_arbdemux(rst, clk, (self.snk_ready, self.snk_valid), ls_hs, sel, ARBITER_TYPE)
        if not EXCLUDE_DATA:
            ls_data = [hs_if.get_src_signals()[2:] for hs_if in ls_tx]
            data_demux = HSD.ls_data_demux(sel, self.get_snk_signals()[2:], ls_data)
        return instances()

