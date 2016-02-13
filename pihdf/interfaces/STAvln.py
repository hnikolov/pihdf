from myhdl import *
from pihdf import mylog

from HSD import HSD

import math

from struct import pack, unpack

class STAvln(HSD):
    '''|
    | ST Avalon Interface:
    | A streaming interface for packed data (ready, valid, sop, eop, empty, data, error).
    | Signals ready and valid are the ready and valid signals of the base HSD class.
    | A packet is defined with start-of-packet (sop) and end-of-packet (eop) signals.
    | Signal 'empty' defines the number of bytes in the last data word, which has to be discarded.
    | The error signal indicates during eop whether the current packet must be discarded.
    |________'''
    def __init__(self, data_width, name=None, direction=None, buf_size=0, terminate=False, filedump=None):

        self.data_width = data_width
        
        WIDTH_BYTE = data_width/8
        emptywidth = math.log(WIDTH_BYTE, 2)
        emptywidth = math.ceil(emptywidth)
    
        stavln_fields = [ ("sop",   bool(0))
                        , ("eop",   bool(0)) 
                        , ("empty", intbv(0)[emptywidth:]) 
                        , ("data",  intbv(0)[data_width:])
                        , ("err",   bool(0))]

        # invoke base class constructor
        HSD.__init__(self, data=stavln_fields, name=name, direction=direction, buf_size=buf_size, terminate=terminate, filedump=filedump, lo=-3)


    def getStimuli(self, inData):
        '''|
        | Get stimuli data from file. Overrides the method of the base HSD class
        |________'''
        stim_data_rx = []
        try:
            with open(inData[0]["file"], 'rb') as myfile:
                for line in myfile.readlines():
                    stim_data_rx.append({"payload":line.strip().decode("hex")})
        except IOError:
            mylog.err("Stimuli file not found for " + self.inst_name + ":" + inData[0]["file"])

        return stim_data_rx


    def unpacked_word(self, word):
        '''|
        | Helper function. Used in append()
        |________'''
        num_bytes = len(word)
        if num_bytes == 1:
            packstr = 'B'
        elif num_bytes == 2:
            packstr = '!H'
        elif num_bytes == 4:
            packstr = '!L'
        elif num_bytes == 8:
            packstr = '!Q'
        return unpack(packstr, word)[0]
    

    def append(self, packet_dict, use_dict=False):
        '''|
        | Add a stimuli packet to the source data list. Overrides the method of the base HSD class
        |________'''
        packet = packet_dict["payload"] if use_dict else packet_dict
        packetlen = len(packet)
        word_width = self.data_width/8
        lastiter = packetlen/word_width + (1 if (packetlen % word_width) else 0)    
        
        l = []
        for i in range(lastiter):
            
            # Default, no errors
            err = False 
             
            sop = (i == 0)
            eop = (i == lastiter-1)
            mty = 0 if not eop else (word_width - (packetlen % word_width)) % word_width
            data = packet[:word_width] + ('\x00' * mty) # + padding if mty > 0
            data = self.unpacked_word(data)
            packet = packet[word_width:]
            self.srcDataList.append((sop, eop, mty, data, err))
#             print "Tuple:", (sop, eop, mty, data, err)


    def packed_word(self, int_val, mty, leftJustified=True):
        '''|
        | Helper function. Used in get()
        |________'''
        word_width = self.data_width/8
        if word_width == 1:
            packstr = 'B'
        elif word_width == 2:
            packstr = '!H'
        elif word_width == 4:
            packstr = '!L'
        elif word_width == 8:
            packstr = '!Q'
        # remove pad bytes
        word = pack(packstr, int_val)
        if leftJustified:
            return word[:len(word)-mty]
        else:
            return word[mty:len(word)]


    def hasPacket(self):
        '''|
        | Checks for a complete packet present in the data list
        |________'''
        for i in range(len(self.snkDataList)):
            eop = self.snkDataList[i][1]
            if eop: return True
        return False


    def get(self, use_dict=False):
        '''|
        | Returns a packet from the sink data list. Overrides the method of the base HSD class
        | Before calling, first check the list with hasPacket()
        |________'''
        started = False
        packet = ''
        fdata = ''
        while len(self.snkDataList):
            pkt_tpl = self.snkDataList.pop(0)
    
            sop  = pkt_tpl[0]
            eop  = pkt_tpl[1]
            mty  = pkt_tpl[2]
            data = pkt_tpl[3]
            err  = pkt_tpl[4] # TODO: err not used

            if sop: 
                started = True
                       
            if started: 
                if eop:
                    data = self.packed_word(data, mty)
                    packet += data
                    fdata += data.encode('hex')
                    if self.filedump:
                        with open(self.filename, "a") as f:
                            f.write(fdata + '\n')    
                    return {"payload":packet} if use_dict else packet
                else: 
                    data = self.packed_word(data, 0)
                    packet += data
                    fdata += data.encode('hex')
            else:
                mylog.err('Wrong framing: ' + self.inst_name + ' (' + self.class_name + ')')
