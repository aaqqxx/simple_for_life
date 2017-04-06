#/usr/bin/env/python
#coding=utf-8

__author__ = 'XingHua'

import sys,re,time,os
maxdata = 50000 #单位KB
memfilename = '/tmp/newnetcardtransdata.txt'
netcard = '/proc/net/dev'

def checkfile(filename):
  if os.path.isfile(filename):
    pass
  else:
    f = open(filename, 'w')
    f.write('0')
    f.close()

def get_net_data():
  nc = netcard or '/proc/net/dev'
  fd = open(nc, "r")
  netcardstatus = False
  for line in fd.readlines():
    if line.find("eth0") > 0:
      netcardstatus = True
      field = line.split()
      recv = field[0].split(":")[1]
      recv = recv or field[1]
      send = field[8]
  if not netcardstatus:
    fd.close()
    print 'Please setup your netcard'
    sys.exit()
  fd.close()
  return (float(recv), float(send))

def monfirst(filename):
  nowtime = time.strftime('%m-%d %H:%M',time.localtime(time.time()))
  sec = time.localtime().tm_sec
  if nowtime == '01-01 00:00':
    if sec < 10:
      f = open(filename, 'w')
      f.write('0')
      f.close()

def net_loop():
  (recv, send) = get_net_data()
  checkfile(memfilename)
  monfirst(memfilename)
  lasttransdaraopen = open(memfilename,'r')
  lasttransdata = lasttransdaraopen.readline()
  lasttransdaraopen.close()
  totaltrans = int(lasttransdata) or 0
  while True:
    time.sleep(3)
    (new_recv, new_send) = get_net_data()
    recvdata = (new_recv - recv) / 1024
    senddata = (new_send - send) / 1024
    totaltrans += int(recvdata)
    totaltrans += int(senddata)
    memw = open(memfilename,'w')
    memw.write(str(totaltrans))
    memw.close()
    if totaltrans >= maxdata:
      os.system('init 0')

if __name__ == "__main__":
  net_loop()