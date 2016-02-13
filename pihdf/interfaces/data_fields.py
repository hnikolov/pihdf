from . import *
from myhdl import *

"""
      Hand-shake interface definitions containing different data fields
      Used when constructing instances of HSD or Bus classes
"""

net_fields = [("eth_dst"       , intbv(0)[48:]),
              ("eth_src"       , intbv(0)[48:]),
              ("eth_lentype"   , intbv(0)[16:]),
              ("eth_vtag"      , intbv(0)[16:]),
              ("eth_is_vtagged", bool(0)),
              ("eth_is_raw"    , bool(0)),
              ("eth_is_ip"     , bool(0)),
              ("ip_protocol"   , intbv(0)[8:]),
              ("ip_src"        , intbv(0)[32:]),
              ("ip_dst"        , intbv(0)[32:]),
              ("ip_is_udp"     , bool(0)),
              ("ip_len"        , intbv(0)[16:]),
              ("ip_ttl"        , intbv(0)[8:])]
#-----------------------------------------------------------              

udp_fields = [("udp_src"       , intbv(0)[16:]),
              ("udp_dst"       , intbv(0)[16:]),
              ("udp_len"       , intbv(0)[16:]),
              ("udp_chksum"    , intbv(0)[16:])]
#-----------------------------------------------------------

tcp_fields = [("ip_src"        , intbv(0)[32:]),
              ("ip_dst"        , intbv(0)[32:]),
              ("tcp_src"       , intbv(0)[16:]),
              ("tcp_dst"       , intbv(0)[16:]),
              ("tcp_len"       , intbv(0)[16:]),
              ("tcp_chksum"    , intbv(0)[16:]),
              ("tcp_seqnum"    , intbv(0)[32:]),
              ("tcp_acknum"    , intbv(0)[32:]),
              ("tcp_dataoffset", intbv(0)[ 4:]),
              ("tcp_f_NS"      , bool(0)),
              ("tcp_f_CWR"     , bool(0)),
              ("tcp_f_ECE"     , bool(0)),
              ("tcp_f_URG"     , bool(0)),
              ("tcp_f_ACK"     , bool(0)),
              ("tcp_f_PSH"     , bool(0)),
              ("tcp_f_RST"     , bool(0)),
              ("tcp_f_SYN"     , bool(0)),
              ("tcp_f_FIN"     , bool(0)),
              ("tcp_winsize"   , intbv(0)[16:]),
              ("tcp_urgptr"    , intbv(0)[16:])]
#-----------------------------------------------------------

tcp_cmd_fields  = [("cmd"         , intbv(0)[ 2:]),
                   ("loc_port"    , intbv(0)[16:]),
                   ("frn_port"    , intbv(0)[16:]),
                   ("frn_ip"      , intbv(0)[32:])]
#-----------------------------------------------------------

ipv_fields = [("cmd"           , bool(0)),
              ("ip"            , intbv(0)[32:]),
              ("vlan_pcp"      , intbv(0)[3:]),
              ("vlan_dei"      , bool(0)),
              ("vlan_id"       , intbv(0)[12:])]
#-----------------------------------------------------------

group_fields = [("cmd"         , bool(0)),
                ("ip"          , intbv(0)[32:]),
                ("vlan_id"     , intbv(0)[12:])]
#-----------------------------------------------------------

port_fields = [("cmd" , bool(0)),
               ("port", intbv(0)[16:])]
#-----------------------------------------------------------

payload_fields = [("bytecount" , intbv(0)[16:]),
                  ("checksum"  , intbv(0)[16:])]
#-----------------------------------------------------------

test_fields = [("bit" , bool(0)),
               ("byte", intbv(2, min=-128, max=256)),
               ("word", intbv(0)[16:])]
#-----------------------------------------------------------

axi_wd_fields = [("data"       , intbv(0)[32:]),
                 ("strobes"    , intbv(0)[4:])]
#-----------------------------------------------------------

axi_rd_fields = [("data"       , intbv(0)[21:]),
                 ("response"   , intbv(0)[2:])]
#-----------------------------------------------------------

AXI4LS = lambda : [ HSD(direction = 0, name = "waddr", data = 32),
                    HSD(direction = 0, name = "wdata", data = axi_wd_fields),
                    HSD(direction = 1, name = "wresp", data = 2),
                    HSD(direction = 0, name = "raddr", data = 32),
                    HSD(direction = 1, name = "rdata", data = axi_rd_fields)]
#-----------------------------------------------------------

AXI4LM = lambda : [ HSD(direction = 1, name = "waddr", data = 32),
                    HSD(direction = 1, name = "wdata", data = axi_wd_fields),
                    HSD(direction = 0, name = "wresp", data = 2),
                    HSD(direction = 1, name = "raddr", data = 32),
                    HSD(direction = 0, name = "rdata", data = axi_rd_fields)]
#-----------------------------------------------------------

wd_fields = [("addr", intbv(0)[ 8:]),
             ("data", intbv(0)[32:])]
#-----------------------------------------------------------

SBUS = lambda : [ HSD(direction = 0, name = "wa_wd", data = wd_fields),
                  HSD(direction = 0, name = "raddr", data =  8),
                  HSD(direction = 1, name = "rdata", data = 32)]
#-----------------------------------------------------------
