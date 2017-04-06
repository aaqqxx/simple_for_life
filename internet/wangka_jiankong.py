#coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

import sys,time
from socket import socket
def read_interface(in_file):
    with file(in_file) as f:
        return f.readlines()[2:]
def set_interface(inter_msg):
    dic={}
    for i in xrange(len(inter_msg)):
        dic[inter_msg[i].split(":")[0].strip()]={"in":inter_msg[i].split(":")[1].strip().split()[0],"out":inter_msg[i].split(":")[1].strip().split()[8]}
    return dic
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
delay = 3
sock = socket()
try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
    print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
    sys.exit(1)
while True:
    now = int( time.time() )
    lines=[]
    int1=read_interface("/proc/net/dev")
    inter_dic1=set_interface(int1)
    time.sleep(1)
    int2=read_interface("/proc/net/dev")
    inter_dic2=set_interface(int2)
    print int(inter_dic2[inter_dic2.keys()[1]]["in"]),int(inter_dic1[inter_dic1.keys()[1]]["in"])
    for i in xrange(len(inter_dic1.keys())):
        lines.append("interface.%s_in %s %d" % (inter_dic1.keys()[i],int(inter_dic2[inter_dic2.keys()[i]]["in"])-int(inter_dic1[inter_dic1.keys()[i]]["in"]),now))
        lines.append("interface.%s_out %s %d" % (inter_dic1.keys()[i],int(inter_dic2[inter_dic2.keys()[i]]["out"])-int(inter_dic1[inter_dic1.keys()[i]]["out"]),now))
    message = '\n'.join(lines) + '\n'
    print "sending message\n"
    print '-' * 80
    print message
    sock.sendall(message)
    time.sleep(delay)
